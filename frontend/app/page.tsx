"use client";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { useEffect, useRef, useState } from "react";

type Msg = { role: "user" | "assistant"; content: string };

export default function ChatPage() {
  const [history, setHistory] = useState<Msg[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom whenever history changes
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [history]);

  async function send() {
    if (!input.trim() || isLoading) return;

    // Optimistic UI update
    setHistory(h => [...h, { role: "user", content: input }]);
    const prompt = input;
    setInput("");
    setIsLoading(true);

    try {
      console.log('Sending request to:', `${process.env.NEXT_PUBLIC_API_URL}/chat`);
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt })
      });

      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }

      const data = await res.json();
      console.log('Response received:', data);
      setHistory(h => [...h, { role: "assistant", content: data.answer }]);
    } catch (error) {
      console.error('Error sending message:', error);
      setHistory(h => [...h, {
        role: "assistant",
        content: `Error: ${error instanceof Error ? error.message : 'Failed to send message'}`
      }]);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="mx-auto max-w-lg p-4 space-y-4">
      <h1 className="text-2xl font-bold">Multi Agent Demo</h1>

      <div className="flex flex-col gap-2 h-[60vh] overflow-y-auto border rounded p-2">
        {history.map((m, i) => (
          <Card key={i}
            className={m.role === "user" ? "ml-auto bg-blue-50" : "mr-auto"}>
            <CardContent className="p-2 whitespace-pre-wrap">{m.content}</CardContent>
          </Card>
        ))}
        {isLoading && (
          <Card className="mr-auto">
            <CardContent className="p-2 text-gray-500">AI is thinking...</CardContent>
          </Card>
        )}
        <div ref={bottomRef} />
      </div>

      <div className="flex gap-2">
        <input
          className="flex-1 border rounded px-2"
          placeholder="Ask me anything…"
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === "Enter" && send()}
          disabled={isLoading}
        />
        <Button onClick={send} disabled={isLoading}>
          {isLoading ? "Sending..." : "Send"}
        </Button>
      </div>
    </main>
  );
} 