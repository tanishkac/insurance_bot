import React, { useState, useEffect, useRef } from 'react';

// This component is the main chat interface.
// It receives messages and loading status from App.js.
// onSendMessage is a function to send a new message to the parent.
const ChatWindow = ({ messages, isLoading, onSendMessage }) => {
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);

  // Automatically scroll to the latest message
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]); // Scroll whenever messages update

  // Handle the user clicking the "Send" button or pressing Enter
  const handleSend = () => {
    if (input.trim()) {
      onSendMessage(input);
      setInput('');
    }
  };

  // Allow sending with the Enter key
  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      handleSend();
    }
  };

  return (
    <div className="chat-window">
      <div className="messages-list">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.sender}`}>
            <div className="avatar">{msg.sender === 'user' ? 'You' : 'Bot'}</div>
            <div className="message-content">{msg.text}</div>
          </div>
        ))}
        {isLoading && (
          <div className="message bot">
             <div className="avatar">Bot</div>
            <div className="message-content typing-indicator">
              <span></span><span></span><span></span>
            </div>
          </div>
        )}
        {/* This empty div is the target for our auto-scrolling */}
        <div ref={messagesEndRef} />
      </div>
      <div className="chat-input-area">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask a question about your policy..."
          disabled={isLoading}
        />
        <button onClick={handleSend} disabled={isLoading}>
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatWindow;