import React from 'react';
import './TicketDashboard.css';

const TicketDashboard = ({ tickets, onSelectTicket }) => {
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

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (tickets.length === 0) {
    return (
      <div className="ticket-dashboard">
        <div className="dashboard-header">
          <h2>Ticket Dashboard</h2>
          <p>Track and manage all support tickets</p>
        </div>
        <div className="empty-state">
          <div className="empty-icon">📋</div>
          <h3>No tickets yet</h3>
          <p>Submit a new ticket to get started.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="ticket-dashboard">
      <div className="dashboard-header">
        <h2>Ticket Dashboard</h2>
        <p>Track and manage all support tickets</p>
      </div>

      <div className="tickets-grid">
        {tickets.map((ticket) => {
          const status = getStatusBadge(ticket.status);
          const urgency = ticket.classification
            ? getUrgencyBadge(ticket.classification.urgency)
            : null;

          return (
            <div
              key={ticket.id}
              className="ticket-card"
              onClick={() => onSelectTicket(ticket)}
            >
              <div className="ticket-card-header">
                <span className="ticket-id">{ticket.id}</span>
                <span className={`badge ${status.className}`}>
                  {status.label}
                </span>
              </div>

              <h3 className="ticket-subject">{ticket.subject}</h3>

              <p className="ticket-description">
                {ticket.description.length > 120
                  ? `${ticket.description.substring(0, 120)}...`
                  : ticket.description}
              </p>

              <div className="ticket-meta">
                <div className="meta-item">
                  <span className="meta-label">Category:</span>
                  <span className="meta-value">
                    {ticket.classification?.category || 'Pending'}
                  </span>
                </div>
                {urgency && (
                  <div className="meta-item">
                    <span className="meta-label">Urgency:</span>
                    <span className={`badge ${urgency.className}`}>
                      {urgency.label}
                    </span>
                  </div>
                )}
              </div>

              {ticket.assigned_people && ticket.assigned_people.length > 0 && (
                <div className="assigned-preview">
                  <span className="assigned-label">Assigned to:</span>
                  <div className="assigned-names">
                    {ticket.assigned_people.map((person, idx) => (
                      <span key={idx} className="assigned-name">
                        {person.name}
                        {person.specialization && (
                          <span className="assigned-spec"> ({person.specialization})</span>
                        )}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              <div className="ticket-footer">
                <span className="ticket-email">{ticket.user_email}</span>
                <span className="ticket-date">{formatDate(ticket.created_at)}</span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default TicketDashboard;
