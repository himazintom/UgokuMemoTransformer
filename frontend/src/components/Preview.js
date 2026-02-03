import React, { useState } from 'react';
import './Preview.css';

function Preview({ result }) {
  const [copied, setCopied] = useState(false);

  const handleCopyLink = () => {
    const fullUrl = `${window.location.origin}${result.download_url}`;
    navigator.clipboard.writeText(fullUrl);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = () => {
    window.open(result.download_url, '_blank');
  };

  return (
    <div className="preview-container">
      <div className="result-card">
        <div className="result-header">
          <h2>✓ Transformation Complete!</h2>
          <p className="job-id">Job ID: {result.job_id}</p>
        </div>

        <div className="result-details">
          <div className="detail-item">
            <span className="label">Output File:</span>
            <span className="value">{result.filename}</span>
          </div>

          <div className="detail-item">
            <span className="label">Created:</span>
            <span className="value">
              {new Date(result.timestamp).toLocaleString()}
            </span>
          </div>
        </div>

        <div className="action-buttons">
          <button className="btn btn-primary" onClick={handleDownload}>
            📥 Download
          </button>
          <button
            className="btn btn-secondary"
            onClick={handleCopyLink}
          >
            {copied ? '✓ Copied!' : '📋 Copy Link'}
          </button>
        </div>

        <div className="preview-info">
          <p>Your animated file is ready to download!</p>
          <p className="small">Download links expire after 24 hours</p>
        </div>
      </div>
    </div>
  );
}

export default Preview;
