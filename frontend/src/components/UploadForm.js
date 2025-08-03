import React, { useState } from 'react';
import axios from 'axios';
import './UploadForm.css';

const UploadForm = ({ onUploadSuccess }) => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState(null);
  const [error, setError] = useState(null);
  const [dragActive, setDragActive] = useState(false);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileSelect = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const uploadFile = async () => {
    if (!file) {
      setError('Please select a file first');
      return;
    }

    if (!file.name.endsWith('.xlsx') && !file.name.endsWith('.xls')) {
      setError('Please select an Excel file (.xlsx or .xls)');
      return;
    }

    setUploading(true);
    setError(null);
    setUploadResult(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('/upload/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setUploadResult(response.data);
      onUploadSuccess();
    } catch (err) {
      setError(err.response?.data?.detail || 'Upload failed');
      console.error('Upload error:', err);
    } finally {
      setUploading(false);
    }
  };

  const resetForm = () => {
    setFile(null);
    setUploadResult(null);
    setError(null);
  };

  return (
    <div className="upload-form">
      <h2>Upload Excel File</h2>
      
      <div className="upload-instructions">
        <h3>Instructions:</h3>
        <ul>
          <li>Excel file must contain columns: ID, Name, Contact</li>
          <li>Optional columns: Date, Collected</li>
          <li>If 3 columns (ID, Name, Contact) are filled: record becomes read-only</li>
          <li>If only 2 columns filled and one is ID: record remains editable</li>
          <li>Email column is ignored during import but can be added later</li>
        </ul>
      </div>

      <div 
        className={`upload-area ${dragActive ? 'drag-active' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        {file ? (
          <div className="file-selected">
            <p>Selected file: {file.name}</p>
            <button onClick={() => setFile(null)}>Remove</button>
          </div>
        ) : (
          <div className="upload-prompt">
            <p>Drag and drop an Excel file here, or click to select</p>
            <input
              type="file"
              accept=".xlsx,.xls"
              onChange={handleFileSelect}
              style={{ display: 'none' }}
              id="file-input"
            />
            <label htmlFor="file-input" className="file-input-label">
              Choose File
            </label>
          </div>
        )}
      </div>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {uploadResult && (
        <div className="upload-result">
          <h3>Upload Results:</h3>
          <p><strong>Message:</strong> {uploadResult.message}</p>
          <p><strong>Records Processed:</strong> {uploadResult.records_processed}</p>
          <p><strong>Records Added:</strong> {uploadResult.records_added}</p>
          {uploadResult.errors.length > 0 && (
            <div className="upload-errors">
              <h4>Errors:</h4>
              <ul>
                {uploadResult.errors.map((error, index) => (
                  <li key={index}>{error}</li>
                ))}
              </ul>
            </div>
          )}
          <button onClick={resetForm}>Upload Another File</button>
        </div>
      )}

      <div className="upload-actions">
        <button 
          onClick={uploadFile} 
          disabled={!file || uploading}
          className="upload-button"
        >
          {uploading ? 'Uploading...' : 'Upload File'}
        </button>
      </div>
    </div>
  );
};

export default UploadForm; 