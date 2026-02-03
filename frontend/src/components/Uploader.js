import React, { useRef, useState } from 'react';
import './Uploader.css';

function Uploader({ onFileSelect, disabled }) {
  const fileInputRef = useRef(null);
  const [dragActive, setDragActive] = useState(false);
  const [fileName, setFileName] = useState(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (disabled) return;

    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (disabled) return;

    setDragActive(false);

    const files = e.dataTransfer.files;
    if (files && files.length > 0) {
      const file = files[0];
      setFileName(file.name);
      onFileSelect(file);
    }
  };

  const handleChange = (e) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      const file = files[0];
      setFileName(file.name);
      onFileSelect(file);
    }
  };

  const handleClick = () => {
    if (!disabled) {
      fileInputRef.current?.click();
    }
  };

  return (
    <div className="uploader-container">
      <div
        className={`upload-area ${dragActive ? 'active' : ''} ${disabled ? 'disabled' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={handleClick}
      >
        <input
          ref={fileInputRef}
          type="file"
          onChange={handleChange}
          accept="image/*,video/*"
          style={{ display: 'none' }}
          disabled={disabled}
        />

        <div className="upload-content">
          <div className="upload-icon">📁</div>
          <h2>Drag and drop your file here</h2>
          <p>or click to select</p>
          <p className="supported-formats">
            Supported: JPG, PNG, GIF, MP4, AVI, MOV, WEBM
          </p>
        </div>

        {fileName && (
          <div className="selected-file">
            <p>Selected: <strong>{fileName}</strong></p>
          </div>
        )}
      </div>

      {!fileName && !disabled && (
        <div className="upload-tips">
          <h3>Tips for best results:</h3>
          <ul>
            <li>Use high contrast images for clearer edges</li>
            <li>For videos, keep them under 500MB</li>
            <li>Square or landscape formats work best</li>
          </ul>
        </div>
      )}
    </div>
  );
}

export default Uploader;
