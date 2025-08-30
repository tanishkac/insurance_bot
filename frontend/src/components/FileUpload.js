import React, { useState } from 'react';

const FileUpload = ({ onUploadSuccess }) => {
  const [file, setFile] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile && selectedFile.type === "application/pdf") {
      setFile(selectedFile);
      setError('');
    } else {
      setFile(null);
      setError('Please select a valid PDF file.');
    }
  };

  // This function now makes a real API call to your backend.
  const handleUpload = () => {
    if (!file) {
      setError('Please select a file first.');
      return;
    }

    setIsProcessing(true);
    setError('');

    // We use FormData to send the file to the backend.
    const formData = new FormData();
    formData.append('file', file);

    // The fetch request to your FastAPI server.
    fetch('http://localhost:8000/upload_pdf', {
      method: 'POST',
      body: formData,
    })
    .then(response => {
      // If the response is not OK, we throw an error to be caught later.
      if (!response.ok) {
        return response.json().then(err => { throw new Error(err.detail || 'Upload failed') });
      }
      return response.json();
    })
    .then(data => {
      // On success, we get the document_id from the backend.
      console.log('Upload successful:', data);
      setIsProcessing(false);
      // We pass the document_id to the parent App component.
      onUploadSuccess(data.document_id); 
    })
    .catch(error => {
      // Handle any errors that occurred during the fetch.
      console.error('Upload error:', error);
      setIsProcessing(false);
      setError(error.message || 'Upload failed. Please try again.');
    });
  };

  return (
    <div className="file-upload-container">
      <h2>Upload Your Insurance Policy</h2>
      <p>Please upload your policy document in PDF format to get started.</p>
      
      <input 
        type="file" 
        accept=".pdf" 
        onChange={handleFileChange} 
        className="file-input"
        id="pdf-upload"
      />
      <label htmlFor="pdf-upload" className="file-input-label">
        {file ? file.name : "Choose a PDF file..."}
      </label>

      {error && <p className="error-message">{error}</p>}

      <button onClick={handleUpload} disabled={isProcessing || !file} className="upload-btn">
        {isProcessing ? 'Processing...' : 'Upload and Process'}
      </button>

      {isProcessing && (
        <div className="processing-indicator">
          <p>Analyzing your document. This may take a moment...</p>
          <div className="spinner"></div>
        </div>
      )}
    </div>
  );
};

export default FileUpload;