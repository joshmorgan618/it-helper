import React from 'react';
import './TicketDetail.css';

const TicketDetail = ({ ticket, onClose }) => {
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString('en-US', {
      month: 'long',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getStatusBadge = (status) => {
    const statusMap = {
      'open': { label: 'Open', className: 'status-open' },
      'in_progress': { label: 'In Progress', className: 'status-in-progress' },
      'resolved': { label: 'Resolved', className: 'status-resolved' },
      'closed': { label: 'Closed', className: 'status-closed' }
    };
    return statusMap[status] || { label: status, className: 'status-default' };
  };

  const getUrgencyBadge = (urgency) => {
    const urgencyMap = {
      'critical': { label: 'Critical', className: 'urgency-critical' },
      'high': { label: 'High', className: 'urgency-high' },
      'medium': { label: 'Medium', className: 'urgency-medium' },
      'low': { label: 'Low', className: 'urgency-low' }
    };
    return urgencyMap[urgency] || { label: urgency, className: 'urgency-default' };
  };

  const status = getStatusBadge(ticket.status);
  const urgency = ticket.classification ? getUrgencyBadge(ticket.classification.urgency) : null;

  return (
    <div className="ticket-detail-overlay" onClick={onClose}>
      <div className="ticket-detail" onClick={(e) => e.stopPropagation()}>
        <div className="detail-header">
          <div className="detail-header-top">
            <h2>{ticket.subject}</h2>
            <button className="close-btn" onClick={onClose}>×</button>
          </div>
          <div className="detail-meta">
            <span className="ticket-id">{ticket.id}</span>
            <span className={`badge ${status.className}`}>{status.label}</span>
            {urgency && (
              <span className={`badge ${urgency.className}`}>{urgency.label}</span>
            )}
          </div>
        </div>

        <div className="detail-body">
          <section className="detail-section">
            <h3>Ticket Information</h3>
            <div className="info-grid">
              <div className="info-item">
                <span className="info-label">Submitted By</span>
                <span className="info-value">{ticket.user_email}</span>
              </div>
              <div className="info-item">
                <span className="info-label">Created</span>
                <span className="info-value">{formatDate(ticket.created_at)}</span>
              </div>
              <div className="info-item">
                <span className="info-label">Last Updated</span>
                <span className="info-value">{formatDate(ticket.updated_at)}</span>
              </div>
              {ticket.classification && (
                <>
                  <div className="info-item">
                    <span className="info-label">Category</span>
                    <span className="info-value capitalize">{ticket.classification.category}</span>
                  </div>
                  <div className="info-item">
                    <span className="info-label">Expertise Level</span>
                    <span className="info-value uppercase">{ticket.classification.expertise_level}</span>
                  </div>
                </>
              )}
            </div>
          </section>

          {ticket.assigned_people && ticket.assigned_people.length > 0 && (
            <section className="detail-section">
              <h3>Assigned Specialists</h3>
              <div className="assigned-people-list">
                {ticket.assigned_people.map((person, index) => (
                  <div key={index} className="assigned-person-card">
                    <div className="person-header">
                      <div className="person-info">
                        <span className="person-name">{person.name}</span>
                        <span className="person-email">{person.email}</span>
                      </div>
                      <span className={`badge role-badge role-${person.role}`}>
                        {person.role}
                      </span>
                    </div>
                    <div className="person-details">
                      {person.specialization && (
                        <div className="detail-item">
                          <span className="detail-label">Specialization:</span>
                          <span className="detail-value capitalize">{person.specialization}</span>
                        </div>
                      )}
                      <div className="detail-item">
                        <span className="detail-label">Tier Level:</span>
                        <span className="detail-value uppercase">{person.tier_level}</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </section>
          )}

          <section className="detail-section">
            <h3>Description</h3>
            <p className="description-text">{ticket.description}</p>
          </section>

          {ticket.classification && (
            <section className="detail-section">
              <h3>Classification</h3>
              <p className="section-text">{ticket.classification.reasoning}</p>
            </section>
          )}

          {ticket.diagnosis && (
            <section className="detail-section">
              <h3>Diagnosis</h3>
              <p className="section-text">{ticket.diagnosis.diagnosis}</p>

              {ticket.diagnosis.potential_causes && ticket.diagnosis.potential_causes.length > 0 && (
                <div className="subsection">
                  <h4>Potential Causes</h4>
                  <ul className="detail-list">
                    {ticket.diagnosis.potential_causes.map((cause, index) => (
                      <li key={index}>{cause}</li>
                    ))}
                  </ul>
                </div>
              )}

              {ticket.diagnosis.recommended_tests && ticket.diagnosis.recommended_tests.length > 0 && (
                <div className="subsection">
                  <h4>Recommended Tests</h4>
                  <ul className="detail-list">
                    {ticket.diagnosis.recommended_tests.map((test, index) => (
                      <li key={index}>{test}</li>
                    ))}
                  </ul>
                </div>
              )}
            </section>
          )}

          {ticket.solution && (
            <section className="detail-section solution-section">
              <h3>Solution</h3>
              <div className="solution-content">
                <p className="section-text">{ticket.solution.solution}</p>

                <div className="solution-meta">
                  <div className="solution-meta-item">
                    <span className="meta-label">Estimated Time</span>
                    <span className="meta-value">{ticket.solution.estimated_time}</span>
                  </div>
                  <div className="solution-meta-item">
                    <span className="meta-label">Confidence Level</span>
                    <span className="meta-value capitalize">{ticket.solution.confidence}</span>
                  </div>
                </div>

                {ticket.solution.tools_needed && ticket.solution.tools_needed.length > 0 && (
                  <div className="subsection">
                    <h4>Tools Required</h4>
                    <ul className="detail-list">
                      {ticket.solution.tools_needed.map((tool, index) => (
                        <li key={index}>{tool}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </section>
          )}
        </div>
      </div>
    </div>
  );
};

export default TicketDetail;
