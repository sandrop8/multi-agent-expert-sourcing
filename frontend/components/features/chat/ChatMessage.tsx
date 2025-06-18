import { cn } from "@/lib/utils";

interface ChatMessageProps {
    role: "user" | "assistant";
    content: string;
    isLoading?: boolean;
}

export default function ChatMessage({ role, content, isLoading = false }: ChatMessageProps) {
    if (isLoading) {
        return (
            <div className="mr-auto p-3 rounded-lg shadow-sm bg-muted text-muted-foreground max-w-[85%] animate-pulse">
                AI is analyzing your request...
            </div>
        );
    }

    return (
        <div
            className={cn(
                "p-3 rounded-lg shadow-sm max-w-[85%] whitespace-pre-wrap break-words",
                role === "user"
                    ? "ml-auto bg-primary text-primary-foreground"
                    : "mr-auto bg-muted text-muted-foreground"
            )}
        >
            {content}
        </div>
    );
}
