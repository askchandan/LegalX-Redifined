"use client";

import React, { useState, useRef, useEffect } from "react";

type Message =
  | { role: "user"; content: string }
  | { role: "assistant"; think: string; response: string };

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [input, setInput] = useState("");
  const chatEndRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;
    if (input.trim().toLowerCase() === "clear") {
      setMessages([]);
      setInput("");
      return;
    }
    setMessages((prev) => [
      ...prev,
      { role: "user", content: input },
      { role: "assistant", think: "...", response: "..." }
    ]);
    setIsLoading(true);
    setInput("");
    try {
      const res = await fetch("http://127.0.0.1:8000/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: input }),
      });
      if (!res.body) throw new Error("No response body");
      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });
        let startIndex = 0;
        let braceCount = 0;
        let inString = false;
        let escaped = false;
        for (let i = 0; i < buffer.length; i++) {
          const char = buffer[i];
          if (escaped) {
            escaped = false;
            continue;
          }
          if (char === "\\") {
            escaped = true;
            continue;
          }
          if (char === '"') {
            inString = !inString;
            continue;
          }
          if (!inString) {
            if (char === "{") {
              braceCount++;
            } else if (char === "}") {
              braceCount--;
              if (braceCount === 0) {
                const jsonStr = buffer.slice(startIndex, i + 1);
                try {
                  const data = JSON.parse(jsonStr);
                  if (data.phase === "thinking") {
                    setMessages((prev) => {
                      return prev.map((msg, idx) =>
                        idx === prev.length - 1 && msg.role === "assistant"
                          ? { ...msg, think: data.think || "", response: "..." }
                          : msg
                      );
                    });
                  } else if (data.phase === "response") {
                    setMessages((prev) => {
                      return prev.map((msg, idx) =>
                        idx === prev.length - 1 && msg.role === "assistant"
                          ? { ...msg, think: msg.think, response: data.response || "" }
                          : msg
                      );
                    });
                  } else {
                    setMessages((prev) => {
                      return prev.map((msg, idx) =>
                        idx === prev.length - 1 && msg.role === "assistant"
                          ? { ...msg, think: msg.think, response: data.response || "" }
                          : msg
                      );
                    });
                  }
                } catch (e) {
                  console.error("Parse error:", e);
                }
                buffer = buffer.slice(i + 1);
                startIndex = 0;
                i = -1;
              }
            }
          }
        }
      }
    } catch {
      setMessages((prev) => {
        const filtered = prev.filter((msg, idx) => !(idx === prev.length - 1 && msg.role === "assistant" && msg.response === "..."));
        return [
          ...filtered,
          {
            role: "assistant",
            think: "Error occurred.",
            response: "Sorry, something went wrong. Let me try again.",
          },
        ];
      });
    }
    setIsLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 flex flex-col">
      {/* Header with human touch */}
      <header className="bg-white/90 backdrop-blur-sm border-b border-slate-200/60 px-6 py-5 shadow-sm">
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-gradient-to-br from-blue-400 to-purple-500 rounded-full flex items-center justify-center text-white">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 006.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3" />
              </svg>
            </div>
            <div>
              <h1 className="text-lg font-medium text-slate-800">Legal Assistant</h1>
              <p className="text-xs text-slate-500">Usually responds instantly</p>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-green-400 rounded-full"></div>
            <span className="text-xs text-slate-600">Online</span>
          </div>
        </div>
      </header>

      {/* Chat Container */}
      <div className="flex-1 flex flex-col max-w-4xl mx-auto w-full">
        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-3">
          {messages.length === 0 && (
            <div className="text-center text-slate-500 mt-16 space-y-6">
              <div className="text-5xl">�</div>
              <div className="space-y-2">
                <h2 className="text-xl font-normal text-slate-700">Start a conversation</h2>
                <p className="text-sm text-slate-600 max-w-sm mx-auto leading-relaxed">
                  Ask me anything about legal matters. I&apos;m here to help you understand the law better.
                </p>
              </div>
              <div className="flex justify-center space-x-2 mt-4">
                <div className="px-3 py-1 bg-slate-100 rounded-full text-xs text-slate-600">Legal questions</div>
                <div className="px-3 py-1 bg-slate-100 rounded-full text-xs text-slate-600">Contract review</div>
                <div className="px-3 py-1 bg-slate-100 rounded-full text-xs text-slate-600">Rights & laws</div>
              </div>
            </div>
          )}

          {messages.map((msg, idx) =>
            msg.role === "user" ? (
              <div key={idx} className="flex justify-end mb-1">
                <div className="bg-blue-500 text-white rounded-2xl rounded-br-sm px-4 py-2.5 max-w-xs lg:max-w-md shadow-sm relative">
                  <p className="text-sm leading-relaxed">{msg.content}</p>
                  <div className="absolute -bottom-1 right-3 w-0 h-0 border-l-4 border-l-transparent border-t-4 border-t-blue-500"></div>
                </div>
              </div>
            ) : (
              <div key={idx} className="flex justify-start mb-1">
                <div className="flex items-start space-x-2 max-w-xs lg:max-w-md">
                  <div className="w-6 h-6 bg-gradient-to-br from-slate-400 to-slate-600 rounded-full flex items-center justify-center text-white flex-shrink-0 mt-1">
                    <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                    </svg>
                  </div>
                  <div className="space-y-2">
                    {/* Thinking phase */}
                    {msg.think && msg.think !== "..." && (
                      <div className="bg-slate-100 rounded-2xl rounded-bl-sm px-4 py-2.5 shadow-sm border border-slate-200/60 relative max-w-xs lg:max-w-md">
                        <p className="text-xs text-slate-600 leading-relaxed">
                          <span className="font-medium">Thinking:</span> {msg.think}
                        </p>
                        <div className="absolute -bottom-1 left-3 w-0 h-0 border-r-4 border-r-transparent border-t-4 border-t-slate-100"></div>
                      </div>
                    )}

                    {/* Response */}
                    <div className="bg-white rounded-2xl rounded-bl-sm px-4 py-2.5 shadow-sm border border-slate-200/60 relative">
                      <p className="text-sm text-slate-800 leading-relaxed">
                        {msg.response === "..." ? (
                          <span className="flex space-x-1">
                            <span className="w-1.5 h-1.5 bg-slate-400 rounded-full animate-pulse"></span>
                            <span className="w-1.5 h-1.5 bg-slate-400 rounded-full animate-pulse" style={{animationDelay: '0.2s'}}></span>
                            <span className="w-1.5 h-1.5 bg-slate-400 rounded-full animate-pulse" style={{animationDelay: '0.4s'}}></span>
                          </span>
                        ) : (
                          msg.response
                        )}
                      </p>
                      <div className="absolute -bottom-1 left-3 w-0 h-0 border-r-4 border-r-transparent border-t-4 border-t-white"></div>
                    </div>
                  </div>
                </div>
              </div>
            )
          )}
          <div ref={chatEndRef} />
        </div>

        {/* Input with human touch */}
        <div className="border-t border-slate-200/60 bg-white/95 backdrop-blur-sm p-4">
          <div className="flex items-end space-x-3">
            <div className="flex-1 relative">
              <input
                type="text"
                className="w-full border border-slate-300 rounded-2xl px-4 py-3 pr-12 focus:outline-none focus:ring-1 focus:ring-blue-400 focus:border-blue-400 text-sm text-slate-800 placeholder-slate-400 bg-white"
                placeholder="Type your message..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && sendMessage()}
                disabled={isLoading}
              />
              <button
                className="absolute right-2 top-1/2 transform -translate-y-1/2 w-8 h-8 bg-blue-500 text-white rounded-full hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-offset-1 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
                onClick={sendMessage}
                disabled={isLoading || !input.trim()}
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
              </button>
            </div>
          </div>
          <div className="flex justify-center mt-2">
            <span className="text-xs text-slate-400">Press Enter to send • Type &quot;clear&quot; to reset</span>
          </div>
        </div>
      </div>
    </div>
  );
}