import axios from 'axios';

// Auto-detect API URL based on environment
const API_URL = process.env.NODE_ENV === 'production' 
  ? '/auth' // In production, use relative URL (handled by Vercel rewrites)
  : 'http://localhost:8000/auth'; // In development, use full URL

// Register a new user
export const register = async (username, password) => {
  try {
    const response = await axios.post(`${API_URL}/`, {
      username,
      password
    });
    return response.data;
  } catch (error) {
    throw error.response?.data || { detail: 'An error occurred during registration' };
  }
};

// Login user and get token
export const login = async (username, password) => {
  try {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    
    const response = await axios.post(`${API_URL}/token`, formData);
    
    if (response.data.access_token) {
      localStorage.setItem('token', response.data.access_token);
    }
    return response.data;
  } catch (error) {
    throw error.response?.data || { detail: 'An error occurred during login' };
  }
};

// Get current user
export const getCurrentUser = async () => {
  try {
    const token = localStorage.getItem('token');
    if (!token) {
      throw new Error('No token found');
    }
    
    const response = await axios.get(`${API_URL}/users/me`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    return response.data;
  } catch (error) {
    throw error.response?.data || { detail: 'Failed to fetch user data' };
  }
};

// Logout user
export const logout = () => {
  localStorage.removeItem('token');
}; 