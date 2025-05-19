import React, { useState } from "react";
import logo from './logo.svg';
import './App.css';


function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMsg = { sender: "user", text: input };
    setMessages((msgs) => [...msgs, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: input }),
      });
      const data = await res.json();
      setMessages((msgs) => [
        ...msgs,
        { sender: "bot", text: data.response?.toString() || "No response" },
      ]);
    } catch {
      setMessages((msgs) => [
        ...msgs,
        { sender: "bot", text: "Error contacting server." },
      ]);
    }
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: 400, margin: "40px auto", fontFamily: "Arial, sans-serif" }}>
      <h2>Federal Data Chatbot</h2>
      <div
        style={{
          height: 300,
          overflowY: "auto",
          border: "1px solid #eee",
          padding: 10,
          marginBottom: 10,
          background: "#fafafa",
          borderRadius: 8,
        }}
      >
        {messages.map((msg, i) => (
          <div key={i} style={{ margin: "8px 0", color: msg.sender === "user" ? "#0074d9" : "#111" }}>
            <b>{msg.sender === "user" ? "You" : "Bot"}:</b> {msg.text}
          </div>
        ))}
        {loading && <div>Bot: ...</div>}
      </div>
      <form onSubmit={sendMessage} style={{ display: "flex" }}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          style={{ flex: 1, padding: 8, borderRadius: 4, border: "1px solid #ccc" }}
          placeholder="Type your question..."
          disabled={loading}
        />
        <button
          type="submit"
          style={{
            padding: "8px 16px",
            marginLeft: 8,
            border: "none",
            background: "#0074d9",
            color: "#fff",
            borderRadius: 4,
            cursor: "pointer",
          }}
          disabled={loading}
        >
          Send
        </button>
      </form>
    </div>
  );
}

export default App;
