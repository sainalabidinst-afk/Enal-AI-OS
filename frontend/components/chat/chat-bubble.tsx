import type { Message } from "@/types";

interface ChatBubbleProps {
  message: Message;
}

export function ChatBubble({ message }: ChatBubbleProps) {
  const isUser = message.role === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-[80%] rounded-lg px-4 py-2 ${
          isUser
            ? "bg-[var(--color-accent)] text-white"
            : "bg-[var(--color-bg-tertiary)] text-[var(--color-text-primary)]"
        }`}
      >
        {message.agent && (
          <span className="text-xs opacity-70 block mb-1">[{message.agent}]</span>
        )}
        <p className="text-sm whitespace-pre-wrap">{message.content}</p>
      </div>
    </div>
  );
}
