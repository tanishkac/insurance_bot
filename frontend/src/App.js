import React, { useState, useEffect } from 'react';
import FileUpload from './components/FileUpload';
import ChatWindow from './components/ChatWindow';
import './App.css';

function App() {
  const [isPdfProcessed, setIsPdfProcessed] = useState(false);
  // NEW STATE: We need to store the document ID from the backend.
  const [documentId, setDocumentId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  // This function now receives the document_id from the successful upload.
  const handlePdfUploadSuccess = (docId) => {
    setDocumentId(docId); // Save the document ID
    setIsPdfProcessed(true);
    setMessages([
      { sender: 'bot', text: 'Thank you! Your policy has been processed. How can I help you today?' }
    ]);
  };
  
  // This function now sends chat messages to the backend API.
  const handleSendMessage = (userMessage) => {
    const newUserMessage = { sender: 'user', text: userMessage };
    setMessages(prevMessages => [...prevMessages, newUserMessage]);
    
    setIsLoading(true);

    // Fetch call to the /chat endpoint
    fetch('http://localhost:8000/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      // We send the document_id along with the message.
      body: JSON.stringify({
        document_id: documentId,
        message: userMessage
      })
    })
    .then(response => {
      if (!response.ok) {
        return response.json().then(err => { throw new Error(err.detail || 'Failed to get response') });
      }
      return response.json();
    })
    .then(data => {
      // The response from the backend is in the 'response' key.
      const botResponse = { sender: 'bot', text: data.response };
      setMessages(prevMessages => [...prevMessages, botResponse]);
      setIsLoading(false);
    })
    .catch(error => {
      console.error('Chat error:', error);
      const errorResponse = { sender: 'bot', text: `Error: ${error.message}` };
      setMessages(prevMessages => [...prevMessages, errorResponse]);
      setIsLoading(false);
    });
  };

  // BONUS: Clean up the session on the backend when the user leaves.
  useEffect(() => {
    // This function will be called when the component unmounts (e.g., tab is closed).
    const cleanupSession = () => {
      if (documentId) {
        // We use navigator.sendBeacon for reliability on exit.
        // It sends a small, asynchronous request that doesn't expect a response.
        const formData = new FormData();
        formData.append('document_id', documentId)
        navigator.sendBeacon(`http://localhost:8000/end_session?document_id=${documentId}`, null);
        console.log(`Session cleanup signal sent for document_id: ${documentId}`);
      }
    };

    window.addEventListener('beforeunload', cleanupSession);

    return () => {
      window.removeEventListener('beforeunload', cleanupSession);
    };
  }, [documentId]); // This effect depends on documentId.

  return (
    <div className="App">
      <header className="app-header">
        <h1>Insurance Policy Assistant</h1>
      </header>
      <main className="app-main">
        {isPdfProcessed ? (
          <ChatWindow 
            messages={messages}
            isLoading={isLoading}
            onSendMessage={handleSendMessage} 
          />
        ) : (
          <FileUpload onUploadSuccess={handlePdfUploadSuccess} />
        )}
      </main>
    </div>
  );
}

export default App;