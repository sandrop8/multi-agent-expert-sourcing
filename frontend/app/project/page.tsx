"use client";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { cn } from "@/lib/utils";
import Link from "next/link";
import { useEffect, useRef, useState } from "react";

type Msg = { role: "user" | "assistant"; content: string };

export default function ProjectSubmissionPage() {
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
            // Use build-time environment variable with fallback
            const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

            console.log('API Configuration:');
            console.log('- NEXT_PUBLIC_API_URL:', process.env.NEXT_PUBLIC_API_URL);
            console.log('- Resolved API URL:', apiUrl);
            console.log('- Full request URL:', `${apiUrl}/chat`);

            const res = await fetch(`${apiUrl}/chat`, {
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

            // More specific error handling
            let errorMessage = 'Failed to send message';
            if (error instanceof TypeError && error.message.includes('Failed to fetch')) {
                errorMessage = 'Network error: Cannot connect to backend. Check if NEXT_PUBLIC_API_URL is correct and backend is running.';
            } else if (error instanceof Error) {
                errorMessage = error.message;
            }

            setHistory(h => [...h, {
                role: "assistant",
                content: `Error: ${errorMessage}`
            }]);
        } finally {
            setIsLoading(false);
        }
    }

    return (
        <main className="flex-1 flex flex-col items-center justify-center p-4 md:p-6 relative">
            {/* Golden background overlay to match homepage */}
            <div className="absolute inset-0 bg-gradient-to-br from-amber-100/40 via-orange-100/30 to-amber-200/40"></div>
            <div className="absolute inset-0 bg-gradient-to-t from-orange-200/20 via-transparent to-amber-100/15"></div>

            <div className="relative z-10 w-full h-full flex justify-center">
                <Card className="w-full max-w-2xl h-full md:max-h-[90vh] flex flex-col shadow-xl bg-background">
                    <div className="p-4 border-b flex items-center justify-between">
                        <Link
                            href="/"
                            className="text-sm text-muted-foreground hover:text-primary transition-colors"
                        >
                            ← Back to Home
                        </Link>
                        <h1 className="text-xl font-semibold text-center text-primary flex-1">
                            Project Submission Chat
                        </h1>
                        <div className="w-20"></div> {/* Spacer for centering */}
                    </div>

                    <div className="px-4 py-2 bg-muted/50 border-b">
                        <p className="text-sm text-muted-foreground text-center">
                            Describe your project requirements and our AI will help match you with the right freelancers
                        </p>
                    </div>

                    <ScrollArea className="flex-1 p-4 space-y-4">
                        {history.map((m, i) => (
                            <div
                                key={i}
                                className={cn(
                                    "p-3 rounded-lg shadow-sm max-w-[85%] whitespace-pre-wrap break-words",
                                    m.role === "user"
                                        ? "ml-auto bg-primary text-primary-foreground"
                                        : "mr-auto bg-muted text-muted-foreground"
                                )}>
                                {m.content}
                            </div>
                        ))}
                        {isLoading && (
                            <div className="mr-auto p-3 rounded-lg shadow-sm bg-muted text-muted-foreground max-w-[85%] animate-pulse">
                                AI is analyzing your project requirements...
                            </div>
                        )}
                        <div ref={bottomRef} />
                    </ScrollArea>

                    <div className="p-4 border-t flex items-center gap-2">
                        <Input
                            placeholder="Describe your project, skills needed, timeline, budget..."
                            value={input}
                            onChange={(e: React.ChangeEvent<HTMLInputElement>) => setInput(e.target.value)}
                            onKeyDown={(e: React.KeyboardEvent<HTMLInputElement>) => e.key === "Enter" && send()}
                            disabled={isLoading}
                            className="flex-1"
                        />
                        <Button onClick={send} disabled={isLoading}>
                            {isLoading ? "Analyzing..." : "Submit"}
                        </Button>
                    </div>
                </Card>
            </div>
        </main>
    );
} 