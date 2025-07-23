"use client";
import { useEffect, useRef, useState } from "react";

export default function ChatUI() {
  const [messages, setMessages] = useState<{ role: string; text: string }[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  // Auto scroll to bottom on new message
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const send = async () => {
    if (!input.trim()) return;

    const userMsg = { role: "user", text: input };
    setMessages((m) => [...m, userMsg]);
    setInput("");
    setLoading(true);

    const assistantMsg = { role: "assistant", text: "🤖: " };
    setMessages((prev) => [...prev, assistantMsg]);

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/weather-stream`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input }),
      });

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();

      let fullMessage = "🤖: ";

      while (reader) {
        const { value, done } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        fullMessage += chunk;

        setMessages((prev) => [
          ...prev.slice(0, -1),
          { role: "assistant", text: fullMessage },
        ]);
      }
    } catch (error) {
      console.error("Streaming error:", error);
      setMessages((prev) => [
        ...prev.slice(0, -1),
        { role: "assistant", text: "❌ Error while streaming." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && !loading) send();
  };

  return (
    <main
      className="max-w-2xl mx-auto p-4 space-y-4"
      role="main"
      aria-label="Chat application"
    >
      <section
        className="h-[400px] overflow-y-auto border rounded-lg p-4 bg-white shadow focus:outline-none"
        tabIndex={0}
        aria-label="Message history"
      >
        {messages.map((m, i) => (
          <div
            key={i}
            className={`mb-3 px-4 py-2 rounded-lg text-sm sm:text-base leading-relaxed w-fit max-w-[85%] ${
              m.role === "user"
                ? "ml-auto bg-blue-600 text-white"
                : "mr-auto bg-gray-100 text-gray-800"
            }`}
            aria-label={`${m.role === "user" ? "User" : "Assistant"} message`}
          >
            {m.text}
          </div>
        ))}
        {loading && (
          <div
            className="mr-auto bg-gray-200 text-gray-500 text-sm rounded-lg px-3 py-2 animate-pulse w-fit max-w-[85%]"
            aria-label="Assistant is typing"
          >
            Thinking...
          </div>
        )}
        <div ref={messagesEndRef} />
      </section>

      <form
        className="flex gap-2"
        role="form"
        aria-label="Message input form"
        onSubmit={(e) => {
          e.preventDefault();
          send();
        }}
      >
        <label htmlFor="chat-input" className="sr-only">
          Type your message
        </label>
        <input
          id="chat-input"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyPress}
          placeholder="Type your message..."
          className="flex-1 p-2 border rounded-md shadow focus:outline-none focus:ring-2 focus:ring-blue-400"
          aria-required="true"
        />
        <button
          type="submit"
          disabled={loading || input.trim() === ""}
          className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-400 disabled:opacity-50"
          aria-label="Send message"
        >
          Send
        </button>
      </form>
    </main>
  );
}