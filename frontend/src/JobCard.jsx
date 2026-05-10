import { MapPin, DollarSign, AlertCircle, CheckCircle } from 'lucide-react';

const JobCard = ({ job }) => {
  const { title, company, location, salary, fit_score, fit_reason, missing_skills, apply_url } = job;

  return (
    <div className="job-card">
      <div className="job-header">
        <div>
          <h3 className="job-title">{title}</h3>
          <p className="job-company">{company}</p>
        </div>
        <div className="fit-score-badge">
          {fit_score}/10 Match
        </div>
      </div>

      <div className="job-details">
        <div className="detail-item">
          <MapPin size={16} color="var(--accent-primary)" />
          <span>{location}</span>
        </div>
        <div className="detail-item">
          <DollarSign size={16} color="var(--accent-success)" />
          <span>{salary}</span>
        </div>
      </div>

      <div className="job-reason">
        <strong>Why it's a fit:</strong>
        <p style={{ marginTop: '0.5rem' }}>{fit_reason}</p>
      </div>

      {missing_skills && missing_skills !== 'None' && (
        <div className="job-missing">
          <AlertCircle size={16} style={{ flexShrink: 0, marginTop: '2px' }} />
          <span><strong>Missing Skills:</strong> {missing_skills}</span>
        </div>
      )}

      {(!missing_skills || missing_skills === 'None') && (
        <div className="job-missing" style={{ color: 'var(--accent-success)' }}>
          <CheckCircle size={16} style={{ flexShrink: 0, marginTop: '2px' }} />
          <span><strong>Perfect Match!</strong> No missing skills.</span>
        </div>
      )}

      <a href={apply_url} target="_blank" rel="noopener noreferrer" className="btn-apply">
        Apply Now
      </a>
    </div>
  );
};

export default JobCard;
