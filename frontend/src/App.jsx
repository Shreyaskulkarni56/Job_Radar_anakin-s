import { useState } from 'react';
import './App.css';
import Upload from './Upload';
import JobCard from './JobCard';

function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleDataReceived = (responseData) => {
    setData(responseData);
    setLoading(false);
  };

  return (
    <div className="app-container">
      <header className="header">
        <h1>JobRadar</h1>
        <p>AI-Powered Job Matching based on your Resume</p>
      </header>

      {!data && !loading && (
        <Upload onDataReceived={handleDataReceived} onLoading={setLoading} />
      )}

      {loading && (
        <div className="loading-container">
          <div className="spinner"></div>
          <p className="loading-text">Analyzing your resume & scraping the web...</p>
        </div>
      )}

      {data && !loading && (
        <div className="results-section">
          <h2 style={{ marginBottom: '1.5rem', fontSize: '2rem', color: 'white' }}>Your Profile Insights</h2>
          <div className="profile-card">
            <div className="profile-stat">
              <span className="stat-label">Name</span>
              <span className="stat-value">{data.profile.name || 'N/A'}</span>
            </div>
            <div className="profile-stat">
              <span className="stat-label">Role</span>
              <span className="stat-value">{data.profile.preferred_role || 'N/A'}</span>
            </div>
            <div className="profile-stat">
              <span className="stat-label">Experience</span>
              <span className="stat-value">{data.profile.experience_level || 'N/A'}</span>
            </div>
            <div className="profile-stat">
              <span className="stat-label">Location Preference</span>
              <span className="stat-value">{data.profile.location_preference || 'N/A'}</span>
            </div>
          </div>
          
          <div style={{ marginBottom: '1.5rem' }}>
            <span className="stat-label" style={{ display: 'block', marginBottom: '0.5rem' }}>Skills Extracted:</span>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
              {data.profile.skills && data.profile.skills.map((skill, i) => (
                <span key={i} style={{ background: 'rgba(88, 166, 255, 0.1)', color: 'var(--accent-primary)', padding: '0.25rem 0.75rem', borderRadius: '50px', fontSize: '0.9rem', border: '1px solid rgba(88, 166, 255, 0.3)' }}>
                  {skill}
                </span>
              ))}
            </div>
          </div>

          <h2 style={{ margin: '4rem 0 2rem', fontSize: '2rem', color: 'white', borderBottom: '1px solid var(--border-color)', paddingBottom: '1rem' }}>Top Job Matches</h2>
          
          <div className="jobs-grid">
            {data.jobs.map((job) => (
              <JobCard key={job.id} job={job} />
            ))}
          </div>

          <div style={{ textAlign: 'center', marginTop: '4rem' }}>
            <button 
              className="btn-upload" 
              onClick={() => setData(null)}
              style={{ display: 'inline-block' }}
            >
              Analyze Another Resume
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
