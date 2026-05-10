import { useState } from 'react';
import { UploadCloud, FileText } from 'lucide-react';
import axios from 'axios';

const Upload = ({ onDataReceived, onLoading }) => {
  const [file, setFile] = useState(null);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    onLoading(true);
    const formData = new FormData();
    formData.append('resume', file);

    try {
      const response = await axios.post('http://localhost:8000/api/jobs/search', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      onDataReceived(response.data);
    } catch (error) {
      console.error('Error uploading resume:', error);
      alert('Failed to process resume. Please try again.');
      onLoading(false);
    }
  };

  return (
    <div className="upload-section">
      <div className="upload-card">
        <div className="upload-icon-container">
          <UploadCloud className="upload-icon" />
        </div>
        <h2>Upload your Resume</h2>
        <p style={{ color: 'var(--text-secondary)', margin: '1rem 0 2rem' }}>
          Our AI will extract your skills and find the perfect job matches for you.
        </p>
        
        <div>
          <label className="btn-upload" style={{ display: 'inline-flex', marginBottom: '1rem' }}>
            Choose PDF File
            <input 
              type="file" 
              className="file-input" 
              accept=".pdf" 
              onChange={handleFileChange} 
            />
          </label>
        </div>

        {file && (
          <div className="selected-file">
            <FileText size={18} />
            {file.name}
          </div>
        )}

        <button 
          className="btn-upload" 
          onClick={handleUpload} 
          disabled={!file}
          style={{ width: '100%', justifyContent: 'center', marginTop: '2rem' }}
        >
          Analyze & Find Jobs
        </button>
      </div>
    </div>
  );
};

export default Upload;
