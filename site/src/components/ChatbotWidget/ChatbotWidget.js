import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import './chat-widget.css';

const API_URL = 'http://localhost:8000/chat';

const ChatWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [inputMessage, setInputMessage] = useState('');
  const [messages, setMessages] = useState([
    { sender: 'bot', text: 'Hello! How can I assist you today?' },
  ]);

  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
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
        body: JSON.stringify({ question: userMessage.text }),
      });

      const data = await res.json();
      setMessages((prev) => [...prev, { sender: 'bot', text: data.answer }]);
    } catch {
      setMessages((prev) => [
        ...prev,
        { sender: 'bot', text: 'Error: Could not reach server.' },
      ]);
    }
  };

  const chatVariants = {
    closed: { opacity: 0, scale: 0.8, y: 50 },
    open: {
      opacity: 1,
      scale: 1,
      y: 0,
      transition: { type: 'spring', stiffness: 400, damping: 30 },
    },
  };

  return (
    <div className="chat-container">
      <AnimatePresence>
        {isOpen && (
          <motion.div
            className="chat-window"
            variants={chatVariants}
            initial="closed"
            animate="open"
            exit="closed"
          >
            {/* Header */}
            <div className="chat-header">
              <h3>Support Chat</h3>
              <button onClick={() => setIsOpen(false)}>✕</button>
            </div>

            {/* Messages */}
            <div className="chat-body">
              {messages.map((msg, index) => (
                <div
                  key={index}
                  className={`message-row ${msg.sender}`}
                >
                  <motion.div
                    initial={{ opacity: 0, x: msg.sender === 'user' ? 40 : -40 }}
                    animate={{ opacity: 1, x: 0 }}
                    className={`message-bubble ${msg.sender}`}
                  >
                    {msg.text}
                  </motion.div>
                </div>
              ))}
              <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <form className="chat-input" onSubmit={handleSendMessage}>
              <input
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                placeholder="Type a message..."
              />
              <button type="submit">➤</button>
            </form>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Toggle Button */}
      <motion.button
        className="chat-toggle"
        onClick={() => setIsOpen(!isOpen)}
        animate={{ rotate: isOpen ? 90 : 0 }}
      >
        💬
      </motion.button>
    </div>
  );
};

export default ChatWidget;
