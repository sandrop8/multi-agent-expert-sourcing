import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import React from "react";

interface ChatInputProps {
    value: string;
    onChange: (value: string) => void;
    onSend: () => void;
    disabled?: boolean;
    placeholder?: string;
    sendButtonText?: string;
}

export default function ChatInput({
    value,
    onChange,
    onSend,
    disabled = false,
    placeholder = "Type your message...",
    sendButtonText = "Send"
}: ChatInputProps) {
    const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === "Enter" && !disabled) {
            onSend();
        }
    };

    return (
        <div className="p-4 border-t flex items-center gap-2">
            <Input
                placeholder={placeholder}
                value={value}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) => onChange(e.target.value)}
                onKeyDown={handleKeyDown}
                disabled={disabled}
                className="flex-1"
            />
            <Button onClick={onSend} disabled={disabled || !value.trim()}>
                {disabled ? "..." : sendButtonText}
            </Button>
        </div>
    );
}
