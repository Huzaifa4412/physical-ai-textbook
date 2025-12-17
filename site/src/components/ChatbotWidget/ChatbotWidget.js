import React, { useState, useRef, useEffect } from 'react';
import './chat-widget.css';

const API_URL = 'https://api-deployment-vercel-tau.vercel.app/chat'; // Using the API contract specified in the requirements

const ChatWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [inputMessage, setInputMessage] = useState('');
  const [messages, setMessages] = useState([
    { sender: 'bot', text: 'Hello! I\'m your Physical AI Assistant. How can I help you understand humanoids, perception, control, and systems?' },
  ]);

  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'auto' });
  }, [messages]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!inputMessage.trim()) return;

    const userMessage = { sender: 'user', text: inputMessage.trim() };
    setMessages((prev) => [...prev, userMessage]);
    setInputMessage('');

    try {
      const res = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: userMessage.text,
          metadata: {
            userType: 'engineer',
            context: 'physical-ai-book'
          }
        }),
      });

      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }

      const data = await res.json();
      if (!data || !data.response) {
        throw new Error('Invalid response format from server');
      }

      setMessages((prev) => [...prev, { sender: 'bot', text: data.response }]);
    } catch (error) {
      console.error('Chat error:', error);
      setMessages((prev) => [
        ...prev,
        {
          sender: 'bot',
          text: 'Error: Could not reach the Physical AI Assistant service. Please try again later.'
        },
      ]);
    }
  };

  return (
    <div className="chat-container">
      {isOpen && (
        <div className="chat-window" role="dialog" aria-modal="true" aria-labelledby="chat-header-title">
          {/* Header */}
          <div className="chat-header">
            <h3 id="chat-header-title">Physical AI Assistant</h3>
            <button
              onClick={() => setIsOpen(false)}
              aria-label="Close chat"
              title="Close chat"
            >
              ✕
            </button>
          </div>

          {/* Messages */}
          <div className="chat-body" role="log" aria-live="polite">
            {messages.map((msg, index) => (
              <div
                key={index}
                className={`message-row ${msg.sender}`}
                role="listitem"
              >
                <div
                  className={`message-bubble ${msg.sender}`}
                  aria-label={`${msg.sender === 'bot' ? 'Assistant' : 'You'}: ${msg.text}`}
                >
                  {msg.text}
                </div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <form className="chat-input" onSubmit={handleSendMessage} role="form">
            <input
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              placeholder="Ask about humanoids, perception, control, or systems..."
              aria-label="Type your question for the Physical AI Assistant"
              autoComplete="off"
            />
            <button type="submit" aria-label="Send message" title="Send message">➤</button>
          </form>
        </div>
      )}

      {/* Toggle Button - Floating button in bottom-right corner */}
      <button
        className="chat-toggle"
        onClick={() => setIsOpen(!isOpen)}
        aria-label={isOpen ? "Close Physical AI Assistant" : "Open Physical AI Assistant"}
        aria-expanded={isOpen}
        aria-controls="chat-window"
      >
        🤖
      </button>
    </div>
  );
};

export default ChatWidget;
