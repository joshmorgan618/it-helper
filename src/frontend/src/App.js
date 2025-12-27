import React, { useState, useEffect } from 'react';
import Navigation from './components/Navigation';
import TicketSubmission from './components/TicketSubmission';
import TicketDashboard from './components/TicketDashboard';
import TicketDetail from './components/TicketDetail';
import './App.css';

function App() {
  const [currentView, setCurrentView] = useState('submit');
  const [tickets, setTickets] = useState([]);
  const [selectedTicket, setSelectedTicket] = useState(null);
  const [loading, setLoading] = useState(true);

  // Fetch tickets on component mount
  useEffect(() => {
    const fetchTickets = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/tickets');
        if (response.ok) {
          const data = await response.json();
          setTickets(data);
        } else {
          console.error('Failed to fetch tickets');
        }
      } catch (error) {
        console.error('Error fetching tickets:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchTickets();
  }, []);

  const handleTicketCreated = (ticket) => {
    setTickets([ticket, ...tickets]);
    setSelectedTicket(ticket);
  };

  const handleSelectTicket = (ticket) => {
    setSelectedTicket(ticket);
  };

  const handleCloseDetail = () => {
    setSelectedTicket(null);
  };

  return (
    <div className="app">
      <Navigation currentView={currentView} setCurrentView={setCurrentView} />

      <main className="main-content">
        {currentView === 'submit' && (
          <TicketSubmission onTicketCreated={handleTicketCreated} />
        )}

        {currentView === 'dashboard' && (
          loading ? (
            <div className="loading-state">Loading tickets...</div>
          ) : (
            <TicketDashboard tickets={tickets} onSelectTicket={handleSelectTicket} />
          )
        )}
      </main>

      {selectedTicket && (
        <TicketDetail ticket={selectedTicket} onClose={handleCloseDetail} />
      )}
    </div>
  );
}

export default App;
