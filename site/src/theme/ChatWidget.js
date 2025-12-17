import React, { useState, useEffect, useRef } from 'react';
import {
  MainContainer,
  ChatContainer,
  MessageList,
  Message,
  MessageInput,
  TypingIndicator
} from '@chatscope/chat-ui-kit-react';
import '@chatscope/chat-ui-kit-styles/dist/default/styles.min.css';
import './ChatWidget.css';

const ChatWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    {
      id: 1,
      message: "Hello! I'm your Physical AI Textbook assistant. How can I help you today?",
      sender: "assistant",
      timestamp: new Date()
    }
  ]);
  const [isTyping, setIsTyping] = useState(false);
  const [conversationId, setConversationId] = useState(null);
  const messageListRef = useRef(null);

  // Toggle chat window
  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  // Handle sending a message
  const handleSend = async (message) => {
    if (!message.trim()) return;

    // Add user message to the chat
    const userMessage = {
      id: Date.now(),
      message: message,
      sender: "user",
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setIsTyping(true);

    try {
      // Call the backend API
      const response = await fetch('https://api-deployment-vercel-tau.vercel.app/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: message,
          conversation_id: conversationId
        })
      });

      const data = await response.json();

      if (response.ok) {
        // Update conversation ID if it's a new conversation
        if (!conversationId) {
          setConversationId(data.conversation_id);
        }

        // Add assistant response to the chat
        const assistantMessage = {
          id: Date.now() + 1,
          message: data.response,
          sender: "assistant",
          timestamp: new Date(),
          sources: data.sources
        };

        setMessages(prev => [...prev, assistantMessage]);
      } else {
        // Handle error response
        const errorMessage = {
          id: Date.now() + 1,
          message: "Sorry, I encountered an error. Please try again.",
          sender: "assistant",
          timestamp: new Date()
        };
        setMessages(prev => [...prev, errorMessage]);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        id: Date.now() + 1,
        message: "Sorry, I'm having trouble connecting. Please check your connection.",
        sender: "assistant",
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  // Scroll to bottom of message list when messages change
  useEffect(() => {
    if (messageListRef.current) {
      messageListRef.current.scrollTop = messageListRef.current.scrollHeight;
    }
  }, [messages, isTyping]);

  return (
    <>
      {/* Chat Toggle Button */}
      {!isOpen && (
        <button className="chat-toggle-btn" onClick={toggleChat}>
          💬
        </button>
      )}

      {/* Chat Window */}
      {isOpen && (
        <div className="chat-widget">
          <div className="chat-header">
            <h3>Physical AI Textbook Assistant</h3>
            <button className="close-btn" onClick={toggleChat}>×</button>
          </div>

          <MainContainer>
            <ChatContainer>
              <MessageList ref={messageListRef}>
                {messages.map((msg) => (
                  <Message
                    key={msg.id}
                    model={{
                      message: msg.message,
                      sender: msg.sender,
                      timestamp: msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
                    }}
                    avatarPosition={msg.sender === "user" ? "right" : "left"}
                  >
                    {msg.sender === "assistant" && msg.sources && msg.sources.length > 0 && (
                      <Message.Footer>
                        <div className="sources">
                          <strong>Sources:</strong>
                          <ul>
                            {msg.sources.slice(0, 2).map((source, index) => (
                              <li key={index}>
                                <a href={source.url} target="_blank" rel="noopener noreferrer">
                                  {source.title}
                                </a>
                              </li>
                            ))}
                          </ul>
                        </div>
                      </Message.Footer>
                    )}
                  </Message>
                ))}

                {isTyping && (
                  <Message
                    model={{
                      message: "",
                      sender: "assistant",
                      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
                    }}
                    avatarPosition="left"
                  >
                    <TypingIndicator content="Thinking..." />
                  </Message>
                )}
              </MessageList>

              <MessageInput
                placeholder="Ask about physics concepts, AI applications..."
                onSend={handleSend}
                attachButton={false}
              />
            </ChatContainer>
          </MainContainer>
        </div>
      )}
    </>
  );
};

export default ChatWidget;