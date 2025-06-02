"use client";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { AGUIClient, FileInfo, generateSessionId } from "@/lib/agui-client";
import { AlertCircle, CheckCircle, Loader2, Paperclip, Send, Upload, Wifi, WifiOff } from "lucide-react";
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

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
            <div className="mx-auto max-w-4xl space-y-6">
                {/* Header */}
                <div className="flex items-center justify-between bg-white rounded-lg shadow-sm p-6">
                    <div>
                        <h1 className="text-3xl font-bold text-gray-900">Multi-Agent Expert Sourcing</h1>
                        <p className="text-gray-600 mt-1">Enhanced with AG-UI Protocol</p>
                    </div>
                    <div className="flex items-center gap-3">
                        <Badge
                            variant={isConnected ? "default" : "destructive"}
                            className="flex items-center gap-2"
                        >
                            {isConnected ? <Wifi className="h-3 w-3" /> : <WifiOff className="h-3 w-3" />}
                            {isConnected ? "Connected" : "Disconnected"}
                        </Badge>
                        <Badge variant="outline" className="font-mono">
                            {sessionId.slice(0, 8)}
                        </Badge>
                    </div>
                </div>

                {/* Agent Status */}
                {agentStatus.status !== "idle" && (
                    <Card className="border-l-4 border-l-blue-500 bg-blue-50">
                        <CardContent className="p-4">
                            <div className="flex items-center gap-3">
                                {getStatusIcon(agentStatus.status)}
                                <div>
                                    <div className="font-medium text-blue-900">
                                        {agentStatus.agent && `${agentStatus.agent}`}
                                    </div>
                                    <div className="text-sm text-blue-700">
                                        {agentStatus.message}
                                    </div>
                                </div>
                            </div>
                        </CardContent>
                    </Card>
                )}

                {/* Messages */}
                <Card className="shadow-lg">
                    <CardContent className="p-0">
                        <div className="h-[60vh] overflow-y-auto p-4 space-y-4">
                            {messages.length === 0 && (
                                <div className="text-center py-12 text-gray-500">
                                    <div className="text-6xl mb-4">🤖</div>
                                    <h3 className="text-lg font-medium mb-2">Welcome to Multi-Agent Expert Sourcing</h3>
                                    <p className="text-sm">Ask me anything about homework - I'll route your question to the right specialist!</p>
                                </div>
                            )}

                            {messages.map((message) => (
                                <div
                                    key={message.id}
                                    className={`flex ${message.role === "user" ? "justify-end" :
                                            message.role === "system" ? "justify-center" : "justify-start"
                                        }`}
                                >
                                    <Card
                                        className={`max-w-[80%] ${message.role === "user"
                                                ? "bg-blue-500 text-white border-blue-500"
                                                : message.role === "system"
                                                    ? "bg-yellow-50 border-yellow-200 text-yellow-800"
                                                    : "bg-white border-gray-200"
                                            }`}
                                    >
                                        <CardContent className="p-4">
                                            <div className="flex items-start justify-between gap-2">
                                                <div className="flex-1">
                                                    <div className="whitespace-pre-wrap">{message.content}</div>

                                                    {/* File attachments */}
                                                    {message.files && message.files.length > 0 && (
                                                        <div className="mt-3 space-y-2">
                                                            {message.files.map((file) => (
                                                                <div
                                                                    key={file.id}
                                                                    className="flex items-center gap-2 text-xs bg-black/10 rounded-lg p-2"
                                                                >
                                                                    <Paperclip className="h-3 w-3" />
                                                                    <span className="font-medium">{file.filename}</span>
                                                                    <span className="text-black/60">
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

                                            <div className="mt-2 text-xs opacity-70">
                                                {new Date(message.timestamp).toLocaleTimeString()}
                                            </div>
                                        </CardContent>
                                    </Card>
                                </div>
                            ))}
                            <div ref={bottomRef} />
                        </div>
                    </CardContent>
                </Card>

                {/* File Upload Preview */}
                {uploadedFiles.length > 0 && (
                    <Card className="border-dashed border-2 border-blue-300 bg-blue-50">
                        <CardContent className="p-4">
                            <div className="flex items-center gap-2 mb-3">
                                <Upload className="h-4 w-4 text-blue-600" />
                                <span className="text-sm font-medium text-blue-900">Uploaded Files:</span>
                            </div>
                            <div className="flex flex-wrap gap-2">
                                {uploadedFiles.map((file) => (
                                    <Badge
                                        key={file.id}
                                        variant="secondary"
                                        className="flex items-center gap-2 bg-blue-200 text-blue-800"
                                    >
                                        {file.filename}
                                        <button
                                            onClick={() => removeFile(file.id)}
                                            className="ml-1 text-blue-600 hover:text-blue-800 font-bold"
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
                <Card className="shadow-lg">
                    <CardContent className="p-4">
                        <div className="flex gap-3">
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
                                className="shrink-0"
                            >
                                <Upload className="h-4 w-4" />
                            </Button>

                            <div className="flex-1 relative">
                                <input
                                    className="w-full border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                    placeholder="Ask me anything about homework..."
                                    value={input}
                                    onChange={(e) => setInput(e.target.value)}
                                    onKeyDown={(e) => e.key === "Enter" && handleSend()}
                                    disabled={!isConnected || agentStatus.status !== "idle"}
                                />
                            </div>

                            <Button
                                onClick={handleSend}
                                disabled={!input.trim() || !isConnected || agentStatus.status !== "idle"}
                                className="shrink-0"
                            >
                                <Send className="h-4 w-4" />
                            </Button>
                        </div>
                    </CardContent>
                </Card>

                {/* Footer */}
                <div className="text-center text-sm text-gray-500 bg-white rounded-lg p-4">
                    <div className="flex items-center justify-center gap-4">
                        <span>AG-UI Protocol</span>
                        <span>•</span>
                        <span>Real-time Multi-Agent Communication</span>
                        <span>•</span>
                        <span>File Upload Enabled</span>
                    </div>
                </div>
            </div>
        </div>
    );
} 