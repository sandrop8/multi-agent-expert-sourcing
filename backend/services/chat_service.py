"""
Chat service - business logic for chat functionality
"""

from typing import List
import sqlalchemy as sa
from agents import Runner
from app_agents.chat_agents import supervisor_agent
from models.base import get_engine
from models.chat_models import messages
from schemas.chat_schemas import ChatReq, Msg


class ChatService:
    """Service class for chat-related business logic"""

    def __init__(self):
        self.engine = get_engine()

    async def process_chat(self, chat_request: ChatReq) -> str:
        """Process chat request through agent system and store conversation"""
        try:
            print(f"🔍 Processing request: {chat_request.prompt}")

            # Use supervisor_agent as entry point to multi-agent system
            result = await Runner.run(supervisor_agent, chat_request.prompt)

            answer = result.final_output if result.final_output else "No response"
            print(f"✅ AI Response: {answer}")

            # Store in database
            with self.engine.begin() as conn:
                conn.execute(
                    messages.insert(),
                    [
                        {"role": "user", "content": chat_request.prompt},
                        {"role": "assistant", "content": answer},
                    ],
                )
            print("💾 Stored conversation in database")

            return answer

        except Exception as e:
            print(f"❌ Error in chat processing: {str(e)}")
            # Handle guardrail rejections gracefully
            if "guardrail" in str(e).lower():
                return "Sorry, I can only help with expert sourcing and talent acquisition requests."
            raise e

    def get_chat_history(self, limit: int = 20) -> List[Msg]:
        """Get chat history from database"""
        with self.engine.connect() as conn:
            rows = conn.execute(
                sa.select(messages).order_by(messages.c.id.desc()).limit(limit)
            )
            return [Msg(**dict(r._mapping)) for r in rows][::-1]
