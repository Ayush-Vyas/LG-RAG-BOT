import { useState } from "react";

export default function App() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);

  const askQuestion = async () => {
    if (!question.trim()) return;

    const userMsg = question;

    setMessages((prev) => [
      ...prev,
      { type: "user", text: userMsg }
    ]);

    try {
      const res = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: userMsg,
          top_k: 3,
        }),
      });

      const data = await res.json();

      setMessages((prev) => [
        ...prev,
        {
          type: "bot",
          text: data.answer || "No answer found",
        },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          type: "bot",
          text: "⚠️ Backend not reachable",
        },
      ]);
    }

    setQuestion("");
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>LG Manuals AI 🤖</h1>

      <div style={styles.chatBox}>
        {messages.map((msg, i) => (
          <div
            key={i}
            style={msg.type === "user" ? styles.user : styles.bot}
          >
            <p style={{ whiteSpace: "pre-wrap" }}>{msg.text}</p>
          </div>
        ))}
      </div>

      <div style={styles.inputArea}>
        <input
          type="text"
          placeholder="Ask about your LG appliance..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && askQuestion()}
          style={styles.input}
        />
        <button onClick={askQuestion} style={styles.button}>
          Send
        </button>
      </div>
    </div>
  );
}

const styles = {
  container: {
    maxWidth: "800px",
    margin: "auto",
    padding: "20px",
    fontFamily: "Arial",
  },
  title: {
    textAlign: "center",
  },
  chatBox: {
    height: "500px",
    overflowY: "auto",
    border: "1px solid #ccc",
    padding: "10px",
    marginBottom: "10px",
    borderRadius: "10px",
    background: "#fff",
  },
  user: {
    textAlign: "right",
    marginBottom: "10px",
    color: "blue",
  },
  bot: {
    textAlign: "left",
    marginBottom: "10px",
    color: "black",
  },
  inputArea: {
    display: "flex",
    gap: "10px",
  },
  input: {
    flex: 1,
    padding: "10px",
    borderRadius: "8px",
    border: "1px solid #ccc",
  },
  button: {
    padding: "10px 20px",
    borderRadius: "8px",
    border: "none",
    background: "#007bff",
    color: "white",
    cursor: "pointer",
  },
};