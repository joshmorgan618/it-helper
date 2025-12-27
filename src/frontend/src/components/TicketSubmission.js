import React, { useState } from 'react';
import './TicketSubmission.css';

const TicketSubmission = ({ onTicketCreated }) => {
  const [formData, setFormData] = useState({
    email: '',
    subject: '',
    description: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:5000/api/tickets', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_email: formData.email,
          subject: formData.subject,
          description: formData.description
        }),
      });

      if (response.ok) {
        const result = await response.json();
        const fullTicketResponse = await fetch(`http://localhost:5000/api/tickets/${result.ticket_id}`);
        const fullTicket = await fullTicketResponse.json();

        setFormData({ email: '', subject: '', description: '' });
        onTicketCreated(fullTicket);
      } else {
        const errorData = await response.json();
        setError(errorData.message || 'Failed to create ticket');
      }
    } catch (err) {
      setError('Unable to connect to the server. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="ticket-submission">
      <div className="submission-header">
        <h2>Submit Support Ticket</h2>
        <p>Describe your issue and our system will analyze and assign it to the appropriate team.</p>
      </div>

      {error && (
        <div className="alert alert-error">
          <span className="alert-icon">!</span>
          <span>{error}</span>
        </div>
      )}

      <form onSubmit={handleSubmit} className="ticket-form">
        <div className="form-group">
          <label htmlFor="email">Email Address</label>
          <input
            id="email"
            name="email"
            type="email"
            value={formData.email}
            onChange={handleChange}
            placeholder="your.email@company.com"
            required
            disabled={loading}
          />
        </div>

        <div className="form-group">
          <label htmlFor="subject">Subject</label>
          <input
            id="subject"
            name="subject"
            type="text"
            value={formData.subject}
            onChange={handleChange}
            placeholder="Brief summary of the issue"
            required
            disabled={loading}
          />
        </div>

        <div className="form-group">
          <label htmlFor="description">Description</label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            placeholder="Provide detailed information about the issue, including any error messages and steps to reproduce..."
            required
            rows="8"
            disabled={loading}
          />
        </div>

        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? (
            <>
              <span className="spinner-small"></span>
              Processing...
            </>
          ) : (
            'Submit Ticket'
          )}
        </button>
      </form>
    </div>
  );
};

export default TicketSubmission;
