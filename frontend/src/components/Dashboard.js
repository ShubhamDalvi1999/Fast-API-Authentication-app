import React, { useState, useEffect } from 'react';
import { getCurrentUser } from '../services/authService';

const Dashboard = () => {
  const [userData, setUserData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const data = await getCurrentUser();
        setUserData(data);
      } catch (err) {
        setError(err.detail || 'Failed to fetch user data');
      } finally {
        setLoading(false);
      }
    };

    fetchUserData();
  }, []);

  if (loading) {
    return (
      <div className="auth-card" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '200px' }}>
        <div className="loading-spinner"></div>
      </div>
    );
  }

  if (error) {
    return <div className="auth-card"><div className="error">{error}</div></div>;
  }

  return (
    <div className="auth-card">
      <h2>Dashboard</h2>
      {userData && (
        <div className="dashboard-content">
          <div className="user-info">
            <div className="user-avatar">
              {userData.username.charAt(0).toUpperCase()}
            </div>
            <div className="user-details">
              <h3>Welcome, {userData.username}!</h3>
              <p className="user-id">User ID: {userData.id}</p>
            </div>
          </div>
          
          <div className="stats-container">
            <div className="stat-card">
              <h4>Account Status</h4>
              <p className="stat-value">Active</p>
            </div>
            <div className="stat-card">
              <h4>Last Login</h4>
              <p className="stat-value">Just Now</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard; 