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
  const [numColors, setNumColors] = useState(8);
  const [pixelSize, setPixelSize] = useState(4);

  const memoStyles = {
    classic: { name: 'Classic Memo', num_colors: 8, pixel_size: 4 },
    minimalist: { name: 'Minimalist B&W', num_colors: 2, pixel_size: 3 },
    detailed: { name: 'Detailed Colors', num_colors: 16, pixel_size: 2 },
    heavy_dots: { name: 'Heavy Dots', num_colors: 6, pixel_size: 6 },
    fine_dots: { name: 'Fine Dots', num_colors: 10, pixel_size: 2 },
  };

  const handleStyleChange = (style) => {
    if (memoStyles[style]) {
      setNumColors(memoStyles[style].num_colors);
      setPixelSize(memoStyles[style].pixel_size);
    }
  };

  const handleFileUpload = async (file) => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('format', outputFormat);
      formData.append('num_colors', numColors);
      formData.append('pixel_size', pixelSize);

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
          <div className="control-group">
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

          <div className="control-group">
            <label>Memo Style Presets:</label>
            <div className="style-buttons">
              {Object.entries(memoStyles).map(([key, style]) => (
                <button
                  key={key}
                  className={`style-btn ${numColors === style.num_colors && pixelSize === style.pixel_size ? 'active' : ''}`}
                  onClick={() => handleStyleChange(key)}
                  disabled={loading}
                >
                  {style.name}
                </button>
              ))}
            </div>
          </div>

          <div className="control-group">
            <label htmlFor="colors-slider">
              Colors: <span className="value">{numColors}</span>
            </label>
            <input
              id="colors-slider"
              type="range"
              min="2"
              max="256"
              value={numColors}
              onChange={(e) => setNumColors(parseInt(e.target.value))}
              disabled={loading}
              className="slider"
            />
          </div>

          <div className="control-group">
            <label htmlFor="pixel-slider">
              Pixel Size: <span className="value">{pixelSize}</span>
            </label>
            <input
              id="pixel-slider"
              type="range"
              min="1"
              max="8"
              value={pixelSize}
              onChange={(e) => setPixelSize(parseInt(e.target.value))}
              disabled={loading}
              className="slider"
            />
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
