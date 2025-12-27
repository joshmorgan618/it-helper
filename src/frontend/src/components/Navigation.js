import React from 'react';
import './Navigation.css';

const Navigation = ({ currentView, setCurrentView }) => {
  return (
    <nav className="navigation">
      <div className="nav-container">
        <div className="nav-brand">
          <h1>IT Support Portal</h1>
        </div>
        <div className="nav-links">
          <button
            className={`nav-link ${currentView === 'dashboard' ? 'active' : ''}`}
            onClick={() => setCurrentView('dashboard')}
          >
            Dashboard
          </button>
          <button
            className={`nav-link ${currentView === 'submit' ? 'active' : ''}`}
            onClick={() => setCurrentView('submit')}
          >
            Submit Ticket
          </button>
        </div>
      </div>
    </nav>
  );
};

export default Navigation;
