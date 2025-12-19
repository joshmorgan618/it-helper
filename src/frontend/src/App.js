import React, { useState } from 'react';
import './App.css';

function App() {
  const [email, setEmail] = useState('');
  const [subject, setSubject] = useState('');
  const [description, setDescription] = useState('');
  const [solution, setSolution] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setSolution(null);

    const data = { 
      user_email: email,
      subject: subject,
      description: description
    };

    try {
      const response = await fetch('http://localhost:5000/api/tickets', { 
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (response.ok) {
        const result = await response.json();
        console.log('Success:', result);
        
        // Fetch full ticket details with complete solution
        const fullTicketResponse = await fetch(`http://localhost:5000/api/tickets/${result.ticket_id}`);
        const fullTicket = await fullTicketResponse.json();
        
        setSolution(fullTicket);
        
        // Clear form
        setEmail('');
        setSubject('');
        setDescription('');
      } else {
        const error = await response.json();
        console.error('Failed:', error);
        alert('Failed to create ticket');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Error connecting to server');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <div className="container">
        <header className="header">
          <h1>Test</h1>
          <p className="subtitle">Test</p>
        </header>

        <div className="card">
          <h2>Submit a Support Ticket</h2>
          <form onSubmit={handleSubmit} className="form">
            <div className="form-group">
              <label htmlFor="email">Email Address</label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="john.doe@company.com"
                required
                disabled={loading}
              />
            </div>

            <div className="form-group">
              <label htmlFor="subject">Subject</label>
              <input
                id="subject"
                type="text"
                value={subject}
                onChange={(e) => setSubject(e.target.value)}
                placeholder="Brief description of your issue"
                required
                disabled={loading}
              />
            </div>

            <div className="form-group">
              <label htmlFor="description">Description</label>
              <textarea
                id="description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Describe your issue in detail..."
                required
                rows="5"
                disabled={loading}
              />
            </div>

            <button type="submit" className="submit-btn" disabled={loading}>
              {loading ? 'Processing...' : 'Submit Ticket'}
            </button>
          </form>
        </div>

        {loading && (
          <div className="card processing-card">
            <div className="processing-header">
              <div className="spinner"></div>
              <h3>Processing Your Ticket</h3>
            </div>
          </div>
        )}

        {solution && !loading && (
          <div className="card solution-card">
            <div className="success-header">
              <span className="success-icon">✅</span>
              <div>
                <h2>Ticket Created Successfully</h2>
                <p className="ticket-id">Ticket ID: {solution.id}</p>
              </div>
            </div>

            <div className="info-grid">
              <div className="info-item category-item">
                <span className="label">Category</span>
                <span className="value">{solution.classification?.category || 'N/A'}</span>
              </div>
              <div className="info-item urgency-item">
                <span className="label">Urgency</span>
                <span className={`value urgency-${solution.classification?.urgency}`}>
                  {solution.classification?.urgency || 'N/A'}
                </span>
              </div>
              <div className="info-item status-item">
                <span className="label">Status</span>
                <span className="value">{solution.status}</span>
              </div>
            </div>

            {solution.classification && (
              <div className="solution-section">
                <h3>Classification</h3>
                <div className="solution-content">
                  <p><strong>Expertise Level:</strong> {solution.classification.expertise_level}</p>
                  <p><strong>Reasoning:</strong> {solution.classification.reasoning}</p>
                </div>
              </div>
            )}

            {solution.diagnosis && (
              <div className="solution-section">
                <h3>Diagnosis</h3>
                <div className="solution-content">
                  <p>{solution.diagnosis.diagnosis}</p>
                  
                  {solution.diagnosis.potential_causes && Array.isArray(solution.diagnosis.potential_causes) && solution.diagnosis.potential_causes.length > 0 && (
                    <div style={{ marginTop: '15px' }}>
                      <strong>Potential Causes:</strong>
                      <ul style={{ marginTop: '8px', paddingLeft: '20px' }}>
                        {solution.diagnosis.potential_causes.map((cause, index) => (
                          <li key={index} style={{ marginBottom: '5px' }}>{cause}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {solution.diagnosis.recommended_tests && Array.isArray(solution.diagnosis.recommended_tests) && solution.diagnosis.recommended_tests.length > 0 && (
                    <div style={{ marginTop: '15px' }}>
                      <strong>Recommended Tests:</strong>
                      <ul style={{ marginTop: '8px', paddingLeft: '20px' }}>
                        {solution.diagnosis.recommended_tests.map((test, index) => (
                          <li key={index} style={{ marginBottom: '5px' }}>{test}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </div>
            )}

            {solution.solution && (
              <div className="solution-section" style={{ background: '#d4edda' }}>
                <h3>Complete Solution</h3>
                <div className="solution-content">
                  <p style={{ marginBottom: '15px', fontSize: '1.1rem', lineHeight: '1.8' }}>
                    {solution.solution.solution}
                  </p>
                  
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px', marginTop: '20px' }}>
                    <div>
                      <strong>Estimated Time:</strong>
                      <p style={{ marginTop: '5px' }}>{solution.solution.estimated_time}</p>
                    </div>
                    <div>
                      <strong>Confidence:</strong>
                      <p style={{ marginTop: '5px', textTransform: 'capitalize' }}>{solution.solution.confidence}</p>
                    </div>
                  </div>

                  {solution.solution.tools_needed && Array.isArray(solution.solution.tools_needed) && solution.solution.tools_needed.length > 0 && (
                    <div style={{ marginTop: '20px' }}>
                      <strong>Tools Needed:</strong>
                      <ul style={{ marginTop: '8px', paddingLeft: '20px' }}>
                        {solution.solution.tools_needed.map((tool, index) => (
                          <li key={index} style={{ marginBottom: '5px' }}>{tool}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </div>
            )}


            <button 
              onClick={() => setSolution(null)} 
              className="new-ticket-btn"
            >
              Submit Another Ticket
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;