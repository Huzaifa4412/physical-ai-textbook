import React, { useState, useRef, useEffect } from 'react';
import './chat-widget.css';
import { LuBotMessageSquare } from 'react-icons/lu';
import { motion, AnimatePresence } from 'motion/react';

const API_URL = 'https://api-deployment-vercel-tau.vercel.app/chat';

const ChatWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const [messages, setMessages] = useState([
    {
      id: crypto.randomUUID(),
      sender: 'bot',
      text:
        "Hello! I'm your Physical AI Assistant. How can I help you understand humanoids, perception, control, and systems?",
    },
  ]);

  const messagesEndRef = useRef(null);

  /* -------------------- AUTO SCROLL -------------------- */
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages.length, isLoading]);

  /* -------------------- SEND MESSAGE -------------------- */
  const handleSendMessage = async (e) => {
    e.preventDefault();

    const text = inputMessage.trim();
    if (!text || isLoading) return;

    setMessages((prev) => [
      ...prev,
      { id: crypto.randomUUID(), sender: 'user', text },
    ]);

    setInputMessage('');
    setIsLoading(true);

    try {
      const res = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: text }),
      });

      if (!res.ok) throw new Error(`HTTP ${res.status}`);

      const data = await res.json();

      if (typeof data?.answer !== 'string') {
        throw new Error('Invalid API response');
      }

      setMessages((prev) => [
        ...prev,
        {
          id: crypto.randomUUID(),
          sender: 'bot',
          text: data.answer,
        },
      ]);
    } catch (err) {
      console.error(err);
      setMessages((prev) => [
        ...prev,
        {
          id: crypto.randomUUID(),
          sender: 'bot',
          text: 'Error: Unable to reach the AI service.',
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  /* -------------------- UI -------------------- */
  return (
    <div className="chat-container">
      <AnimatePresence>
        {isOpen && (
          <motion.div
            id="chat-window"
            className="chat-window"
            role="dialog"
            aria-modal="true"
            aria-labelledby="chat-header-title"
            initial={{ opacity: 0, scale: 0.95, y: 40 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 40 }}
            transition={{ duration: 0.25, ease: 'easeOut' }}
          >
            {/* Header */}
            <div className="chat-header">
              <h3 id="chat-header-title">Physical AI Assistant</h3>
              <button onClick={() => setIsOpen(false)}>✕</button>
            </div>

            {/* Messages */}
            <div className="chat-body" role="log" aria-relevant="additions">
              {messages.map((msg) => (
                <motion.div
                  key={msg.id}
                  className={`message-row ${msg.sender}`}
                  initial={{ opacity: 0, y: 12 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.2 }}
                >
                  <div className={`message-bubble ${msg.sender}`}>
                    {msg.text}
                  </div>
                </motion.div>
              ))}

              {isLoading && (
                <motion.div
                  className="message-row bot"
                  animate={{ opacity: [0.4, 1, 0.4] }}
                  transition={{ repeat: Infinity, duration: 1.2 }}
                >
                  <div className="message-bubble bot">Thinking…</div>
                </motion.div>
              )}

              <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <form className="chat-input" onSubmit={handleSendMessage}>
              <input
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                placeholder="Ask about humanoids, perception, control, or systems..."
                disabled={isLoading}
              />
              <button type="submit" disabled={isLoading}>
                ➤
              </button>
            </form>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Toggle Button */}
      <motion.button
        className="chat-toggle"
        onClick={() => setIsOpen((v) => !v)}
        aria-expanded={isOpen}
        aria-controls="chat-window"
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.95 }}
      >
        <LuBotMessageSquare />
      </motion.button>
    </div>
  );
};

export default ChatWidget;
