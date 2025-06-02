"use client";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { AGUIClient, FileInfo, generateSessionId } from "@/lib/agui-client";
import { AlertCircle, CheckCircle, Loader2, Paperclip, Send, Upload } from "lucide-react";
import React, { useCallback, useEffect, useRef, useState } from "react";

interface Message {
    id: string;
    role: "user" | "assistant" | "system";
    content: string;
    timestamp: string;
    files?: FileInfo[];
    agent?: string;
    status?: "thinking" | "processing" | "completed" | "blocked" | "error";
}

interface AgentStatus {
    status: "idle" | "thinking" | "processing" | "responding" | "error";
    message?: string;
    agent?: string;
}

export default function AGUIChat() {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState("");
    const [agentStatus, setAgentStatus] = useState<AgentStatus>({ status: "idle" });
    const [uploadedFiles, setUploadedFiles] = useState<FileInfo[]>([]);
    const [isConnected, setIsConnected] = useState(false);
    const [sessionId] = useState(() => generateSessionId());

    const clientRef = useRef<AGUIClient | null>(null);
    const bottomRef = useRef<HTMLDivElement>(null);
    const fileInputRef = useRef<HTMLInputElement>(null);

    // Initialize AG-UI client
    useEffect(() => {
        const baseUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
        const client = new AGUIClient(baseUrl, sessionId);
        clientRef.current = client;

        // Set up event handlers
        client.on("onConnectionEstablished", (data: any) => {
            console.log("🔌 AG-UI Connection established:", data);
            setIsConnected(true);
            addSystemMessage("Connected to AG-UI Multi-Agent System", data.features);
        });

        client.on("onAgentThinking", (data: any) => {
            console.log("🤔 Agent thinking:", data);
            setAgentStatus({
                status: "thinking",
                message: data.message,
                agent: data.agent
            });
        });

        client.on("onAgentProcessing", (data: any) => {
            console.log("⚙️ Agent processing:", data);
            setAgentStatus({
                status: "processing",
                message: data.message,
                agent: data.agent
            });
        });

        client.on("onAgentResponse", (data: any) => {
            console.log("💬 Agent response:", data);
            setAgentStatus({
                status: "responding",
                message: "Responding...",
                agent: data.agent
            });

            addMessage({
                id: Date.now().toString(),
                role: "assistant",
                content: data.content,
                timestamp: new Date().toISOString(),
                agent: data.agent,
                status: data.status
            });

            // Reset agent status after response
            setTimeout(() => {
                setAgentStatus({ status: "idle" });
            }, 1000);
        });

        client.on("onFileUploaded", (data: any) => {
            console.log("📁 File uploaded:", data);
            addSystemMessage(`File uploaded: ${data.file.filename}`, [data.file]);
        });

        client.on("onTaskCompleted", (data: any) => {
            console.log("✅ Task completed:", data);
            setAgentStatus({ status: "idle" });
        });

        client.on("onError", (data: any) => {
            console.error("❌ AG-UI Error:", data);
            setAgentStatus({
                status: "error",
                message: data.message
            });

            addMessage({
                id: Date.now().toString(),
                role: "system",
                content: `Error: ${data.message}`,
                timestamp: new Date().toISOString(),
                status: "error"
            });
        });

        client.on("onDisconnected", () => {
            console.log("🔌 AG-UI Disconnected");
            setIsConnected(false);
            setAgentStatus({ status: "error", message: "Connection lost" });
        });

        // Connect to WebSocket
        client.connect();
        client.startHeartbeat();

        // Cleanup on unmount
        return () => {
            client.disconnect();
        };
    }, [sessionId]);

    // Auto-scroll to bottom
    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);

    const addMessage = useCallback((message: Message) => {
        setMessages(prev => [...prev, message]);
    }, []);

    const addSystemMessage = useCallback((content: string, data?: any) => {
        addMessage({
            id: Date.now().toString(),
            role: "system",
            content,
            timestamp: new Date().toISOString(),
            files: data?.length ? data : undefined
        });
    }, [addMessage]);

    const handleSend = async () => {
        if (!input.trim() || !isConnected || !clientRef.current) return;

        const userMessage: Message = {
            id: Date.now().toString(),
            role: "user",
            content: input,
            timestamp: new Date().toISOString(),
            files: uploadedFiles.length > 0 ? uploadedFiles : undefined
        };

        // Add user message to chat
        addMessage(userMessage);

        // Clear input and files
        const messageContent = input;
        setInput("");
        setUploadedFiles([]);

        try {
            // Send message through AG-UI protocol
            await clientRef.current.sendChatMessage(messageContent, {
                uploaded_files: uploadedFiles
            });
        } catch (error) {
            console.error("❌ Error sending message:", error);
            addMessage({
                id: Date.now().toString(),
                role: "system",
                content: `Failed to send message: ${error}`,
                timestamp: new Date().toISOString(),
                status: "error"
            });
        }
    };

    const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
        const files = event.target.files;
        if (!files || !clientRef.current) return;

        for (const file of Array.from(files)) {
            try {
                setAgentStatus({
                    status: "processing",
                    message: `Uploading ${file.name}...`
                });

                const fileInfo = await clientRef.current.uploadFile(file);
                setUploadedFiles(prev => [...prev, fileInfo]);

                setAgentStatus({ status: "idle" });
            } catch (error) {
                console.error("❌ File upload error:", error);
                setAgentStatus({
                    status: "error",
                    message: `Upload failed: ${error}`
                });
            }
        }

        // Reset file input
        if (fileInputRef.current) {
            fileInputRef.current.value = "";
        }
    };

    const removeFile = (fileId: string) => {
        setUploadedFiles(prev => prev.filter(f => f.id !== fileId));
    };

    const getStatusIcon = (status?: string) => {
        switch (status) {
            case "thinking":
            case "processing":
                return <Loader2 className="h-4 w-4 animate-spin text-blue-500" />;
            case "completed":
                return <CheckCircle className="h-4 w-4 text-green-500" />;
            case "blocked":
            case "error":
                return <AlertCircle className="h-4 w-4 text-red-500" />;
            default:
                return null;
        }
    };

    const getStatusColor = (status?: string) => {
        switch (status) {
            case "thinking":
            case "processing":
                return "bg-blue-100 text-blue-800";
            case "completed":
                return "bg-green-100 text-green-800";
            case "blocked":
            case "error":
                return "bg-red-100 text-red-800";
            default:
                return "bg-gray-100 text-gray-800";
        }
    };

    return (
        <main className="mx-auto max-w-4xl p-4 space-y-4">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-2xl font-bold">Multi-Agent Expert Sourcing</h1>
                    <p className="text-sm text-gray-600">Enhanced with AG-UI Protocol</p>
                </div>
                <div className="flex items-center gap-2">
                    <Badge variant={isConnected ? "default" : "destructive"}>
                        {isConnected ? "Connected" : "Disconnected"}
                    </Badge>
                    <Badge variant="outline">Session: {sessionId.slice(0, 8)}</Badge>
                </div>
            </div>

            {/* Agent Status */}
            {agentStatus.status !== "idle" && (
                <Card className="border-l-4 border-l-blue-500">
                    <CardContent className="p-3">
                        <div className="flex items-center gap-2">
                            {getStatusIcon(agentStatus.status)}
                            <span className="text-sm font-medium">
                                {agentStatus.agent && `${agentStatus.agent}: `}
                                {agentStatus.message}
                            </span>
                        </div>
                    </CardContent>
                </Card>
            )}

            {/* Messages */}
            <div className="flex flex-col gap-3 h-[60vh] overflow-y-auto border rounded-lg p-4 bg-gray-50">
                {messages.map((message) => (
                    <Card
                        key={message.id}
                        className={`${message.role === "user"
                            ? "ml-auto bg-blue-50 border-blue-200"
                            : message.role === "system"
                                ? "mx-auto bg-yellow-50 border-yellow-200"
                                : "mr-auto bg-white"
                            } max-w-[80%]`}
                    >
                        <CardContent className="p-3">
                            <div className="flex items-start justify-between gap-2">
                                <div className="flex-1">
                                    <div className="whitespace-pre-wrap">{message.content}</div>

                                    {/* File attachments */}
                                    {message.files && message.files.length > 0 && (
                                        <div className="mt-2 space-y-1">
                                            {message.files.map((file) => (
                                                <div
                                                    key={file.id}
                                                    className="flex items-center gap-2 text-xs bg-gray-100 rounded p-1"
                                                >
                                                    <Paperclip className="h-3 w-3" />
                                                    <span>{file.filename}</span>
                                                    <span className="text-gray-500">
                                                        ({Math.round(file.size / 1024)}KB)
                                                    </span>
                                                </div>
                                            ))}
                                        </div>
                                    )}
                                </div>

                                <div className="flex flex-col items-end gap-1">
                                    {getStatusIcon(message.status)}
                                    {message.agent && (
                                        <Badge variant="outline" className="text-xs">
                                            {message.agent}
                                        </Badge>
                                    )}
                                </div>
                            </div>

                            <div className="mt-1 text-xs text-gray-500">
                                {new Date(message.timestamp).toLocaleTimeString()}
                            </div>
                        </CardContent>
                    </Card>
                ))}
                <div ref={bottomRef} />
            </div>

            {/* File Upload Preview */}
            {uploadedFiles.length > 0 && (
                <Card className="border-dashed">
                    <CardContent className="p-3">
                        <div className="flex items-center gap-2 mb-2">
                            <Upload className="h-4 w-4" />
                            <span className="text-sm font-medium">Uploaded Files:</span>
                        </div>
                        <div className="flex flex-wrap gap-2">
                            {uploadedFiles.map((file) => (
                                <Badge
                                    key={file.id}
                                    variant="secondary"
                                    className="flex items-center gap-1"
                                >
                                    {file.filename}
                                    <button
                                        onClick={() => removeFile(file.id)}
                                        className="ml-1 text-red-500 hover:text-red-700"
                                    >
                                        ×
                                    </button>
                                </Badge>
                            ))}
                        </div>
                    </CardContent>
                </Card>
            )}

            {/* Input */}
            <div className="flex gap-2">
                <input
                    ref={fileInputRef}
                    type="file"
                    multiple
                    onChange={handleFileUpload}
                    className="hidden"
                    accept=".txt,.md,.json,.csv,.pdf"
                />

                <Button
                    variant="outline"
                    onClick={() => fileInputRef.current?.click()}
                    disabled={!isConnected}
                >
                    <Upload className="h-4 w-4" />
                </Button>

                <input
                    className="flex-1 border rounded px-3 py-2"
                    placeholder="Ask me anything about homework..."
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && handleSend()}
                    disabled={!isConnected || agentStatus.status !== "idle"}
                />

                <Button
                    onClick={handleSend}
                    disabled={!input.trim() || !isConnected || agentStatus.status !== "idle"}
                >
                    <Send className="h-4 w-4" />
                </Button>
            </div>

            {/* Footer */}
            <div className="text-center text-xs text-gray-500">
                AG-UI Protocol • Real-time Multi-Agent Communication • File Upload Enabled
            </div>
        </main>
    );
} 