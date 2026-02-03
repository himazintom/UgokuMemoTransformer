import React, { useState } from 'react';
import axios from 'axios';
import Uploader from './components/Uploader';
import Preview from './components/Preview';
import './App.css';

function App() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);
  const [outputFormat, setOutputFormat] = useState('gif');

  const handleFileUpload = async (file) => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('format', outputFormat);

      const response = await axios.post('/api/transform', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'An error occurred during transformation');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>うごくメモ帳</h1>
        <p className="subtitle">Animated Memo Transformer</p>
        <p className="description">Transform your images and videos into animated memo-style</p>
      </header>

      <main className="app-main">
        <div className="controls-section">
          <div className="format-selector">
            <label htmlFor="format-select">Output Format:</label>
            <select
              id="format-select"
              value={outputFormat}
              onChange={(e) => setOutputFormat(e.target.value)}
              disabled={loading}
            >
              <option value="gif">GIF</option>
              <option value="video">Video (MP4)</option>
            </select>
          </div>
        </div>

        <Uploader onFileSelect={handleFileUpload} disabled={loading} />

        {loading && (
          <div className="loading-container">
            <div className="spinner"></div>
            <p>Processing your media...</p>
          </div>
        )}

        {error && (
          <div className="error-message">
            <p>Error: {error}</p>
          </div>
        )}

        {result && (
          <Preview result={result} />
        )}
      </main>

      <footer className="app-footer">
        <p>&copy; 2024 UgokuMemoTransformer. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default App;
