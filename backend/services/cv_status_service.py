"""
CV Status Update Service
Handles progressive status updates during CV processing workflow
Maps backend processing stages to user-friendly messages
"""

import time
from typing import Dict, Any, Optional
from datetime import datetime
from enum import Enum


class CVProcessingStage(Enum):
    """Enumeration of CV processing stages"""

    UPLOAD_STARTED = "upload_started"
    FILE_VALIDATION = "file_validation"
    GUARDRAIL_VALIDATION = "guardrail_validation"
    FILE_PREPARATION = "file_preparation"
    OPENAI_UPLOAD = "openai_upload"
    CV_PARSING = "cv_parsing"
    PROFILE_ENRICHMENT = "profile_enrichment"
    SKILLS_EXTRACTION = "skills_extraction"
    GAP_ANALYSIS = "gap_analysis"
    FINALIZING = "finalizing"
    COMPLETED = "completed"
    ERROR = "error"


class CVStatusUpdate:
    """Model for CV processing status updates"""

    def __init__(
        self,
        stage: CVProcessingStage,
        message: str,
        progress: int = 0,
        details: str = "",
    ):
        self.stage = stage
        self.message = message
        self.progress = progress  # 0-100
        self.details = details
        self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "stage": self.stage.value,
            "message": self.message,
            "progress": self.progress,
            "details": self.details,
            "timestamp": self.timestamp,
        }


class CVStatusManager:
    """Manager for CV processing status updates"""

    def __init__(self):
        # In-memory storage for status updates (could be replaced with Redis/database)
        self._status_storage: Dict[str, list] = {}

        # User-friendly messages for each stage
        self._stage_messages = {
            CVProcessingStage.UPLOAD_STARTED: {
                "message": "Starting CV upload...",
                "progress": 5,
            },
            CVProcessingStage.FILE_VALIDATION: {
                "message": "Validating your CV file...",
                "progress": 10,
            },
            CVProcessingStage.GUARDRAIL_VALIDATION: {
                "message": "Checking document format...",
                "progress": 15,
            },
            CVProcessingStage.FILE_PREPARATION: {
                "message": "Preparing your CV for analysis...",
                "progress": 20,
            },
            CVProcessingStage.OPENAI_UPLOAD: {
                "message": "Uploading to AI processing system...",
                "progress": 30,
            },
            CVProcessingStage.CV_PARSING: {
                "message": "Analyzing your CV content...",
                "progress": 50,
            },
            CVProcessingStage.PROFILE_ENRICHMENT: {
                "message": "Enhancing your professional profile...",
                "progress": 65,
            },
            CVProcessingStage.SKILLS_EXTRACTION: {
                "message": "Identifying your skills and expertise...",
                "progress": 75,
            },
            CVProcessingStage.GAP_ANALYSIS: {
                "message": "Analyzing profile completeness...",
                "progress": 85,
            },
            CVProcessingStage.FINALIZING: {
                "message": "Finalizing your profile analysis...",
                "progress": 95,
            },
            CVProcessingStage.COMPLETED: {
                "message": "CV analysis complete! Your feedback is ready.",
                "progress": 100,
            },
            CVProcessingStage.ERROR: {
                "message": "Something went wrong. Please try again.",
                "progress": 0,
            },
        }

    def update_status(
        self, session_id: str, stage: CVProcessingStage, details: str = ""
    ) -> CVStatusUpdate:
        """Update the processing status for a CV upload session"""

        stage_config = self._stage_messages.get(stage)
        if not stage_config:
            stage_config = {"message": "Processing...", "progress": 50}

        status_update = CVStatusUpdate(
            stage=stage,
            message=stage_config["message"],
            progress=stage_config["progress"],
            details=details,
        )

        # Store the status update
        if session_id not in self._status_storage:
            self._status_storage[session_id] = []
            print(f"🆕 [STATUS] Created new session storage for: {session_id}")

        self._status_storage[session_id].append(status_update.to_dict())

        # Keep only the last 20 status updates per session
        if len(self._status_storage[session_id]) > 20:
            self._status_storage[session_id] = self._status_storage[session_id][-20:]

        # Log the status update with user-friendly message
        print(
            f"📊 [STATUS] {session_id}: {status_update.message} ({status_update.progress}%)"
        )
        print(
            f"🔍 [STATUS] Stage: {stage.value}, Total sessions: {len(self._status_storage)}"
        )
        if details:
            print(f"📝 [STATUS] Details: {details}")

        return status_update

    def get_current_status(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get the current status for a CV upload session"""

        if (
            session_id not in self._status_storage
            or not self._status_storage[session_id]
        ):
            return None

        return self._status_storage[session_id][-1]

    def get_status_history(self, session_id: str) -> list:
        """Get the full status history for a CV upload session"""

        return self._status_storage.get(session_id, [])

    def clear_session(self, session_id: str):
        """Clear status data for a session"""

        if session_id in self._status_storage:
            del self._status_storage[session_id]

    def cleanup_old_sessions(self, max_age_hours: int = 24):
        """Clean up old session data"""

        cutoff_time = datetime.now().timestamp() - (max_age_hours * 3600)

        sessions_to_remove = []
        for session_id, status_list in self._status_storage.items():
            if status_list:
                last_update_time = datetime.fromisoformat(
                    status_list[-1]["timestamp"]
                ).timestamp()
                if last_update_time < cutoff_time:
                    sessions_to_remove.append(session_id)

        for session_id in sessions_to_remove:
            del self._status_storage[session_id]

        if sessions_to_remove:
            print(f"🧹 [STATUS] Cleaned up {len(sessions_to_remove)} old sessions")


# Global status manager instance
cv_status_manager = CVStatusManager()


def generate_session_id(file_name: str = "") -> str:
    """Generate a unique session ID for CV processing"""
    timestamp = str(int(time.time() * 1000))
    file_hash = str(hash(file_name))[-6:] if file_name else "000000"
    return f"cv_{timestamp}_{file_hash}"


def log_status_update(
    session_id: str, stage: CVProcessingStage, details: str = ""
) -> CVStatusUpdate:
    """Helper function to log status updates"""
    return cv_status_manager.update_status(session_id, stage, details)


def get_status_for_frontend(session_id: str) -> Dict[str, Any]:
    """Get status update formatted for frontend consumption"""

    print(f"🔍 [STATUS] Frontend requesting status for session: {session_id}")
    print(
        f"🗄️ [STATUS] Available sessions: {list(cv_status_manager._status_storage.keys())}"
    )

    current_status = cv_status_manager.get_current_status(session_id)

    if not current_status:
        # Session not found - could be a timing issue where polling started before session creation
        # Return a reasonable default instead of causing infinite loops
        print(f"⚠️ [STATUS] Session {session_id} not found - returning default status")
        return {
            "status": "upload_started",
            "message": "Starting CV upload...",
            "progress": 5,
            "details": "Processing is starting, please wait...",
            "timestamp": datetime.now().isoformat(),
        }

    print(
        f"✅ [STATUS] Found status for {session_id}: {current_status['stage']} ({current_status['progress']}%)"
    )

    return {
        "status": current_status["stage"],
        "message": current_status["message"],
        "progress": current_status["progress"],
        "details": current_status.get("details", ""),
        "timestamp": current_status["timestamp"],
    }
