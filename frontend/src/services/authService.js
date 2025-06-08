import axios from 'axios';

const API_URL = 'http://localhost:8000/auth';

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