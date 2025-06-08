import axios from 'axios';

// Auto-detect API URL based on environment
const API_URL = process.env.NODE_ENV === 'production' 
  ? '/api/auth' // In production, use relative URL (handled by Vercel rewrites)
  : 'http://localhost:8000/api/auth'; // In development, use full URL

// Create an axios instance with common settings
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true
});

// Helper function to safely extract error message
const extractErrorMessage = (error) => {
  if (!error) return 'An unknown error occurred';
  
  if (error.response) {
    const { data } = error.response;
    // FastAPI validation errors have a specific format
    if (data && typeof data === 'object') {
      if (data.detail) {
        // If detail is a string, return it
        if (typeof data.detail === 'string') {
          return data.detail;
        }
        // If detail is an array (validation errors), format it
        if (Array.isArray(data.detail)) {
          return data.detail.map(err => `${err.loc.join('.')}: ${err.msg}`).join(', ');
        }
        // If detail is an object, stringify it
        return JSON.stringify(data.detail);
      }
      // Other structured error
      return JSON.stringify(data);
    }
    return data || 'Server error';
  }
  
  if (error.message) return error.message;
  
  return 'An unexpected error occurred';
};

// Register a new user
export const register = async (username, password) => {
  try {
    const response = await api.post('/', {
      username,
      password
    });
    return response.data;
  } catch (error) {
    console.error('Registration error:', error);
    throw extractErrorMessage(error);
  }
};

// Login user and get token
export const login = async (username, password) => {
  try {
    // FastAPI's OAuth2PasswordRequestForm requires x-www-form-urlencoded format
    const params = new URLSearchParams();
    params.append('username', username);
    params.append('password', password);
    
    // Override content-type for this specific request
    const response = await axios.post(`${API_URL}/token`, params, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      withCredentials: true
    });
    
    if (response.data.access_token) {
      localStorage.setItem('token', response.data.access_token);
    }
    return response.data;
  } catch (error) {
    console.error('Login error:', error);
    throw extractErrorMessage(error);
  }
};

// Get current user
export const getCurrentUser = async () => {
  try {
    const token = localStorage.getItem('token');
    if (!token) {
      throw new Error('No token found. Please login again.');
    }
    
    const response = await api.get('/users/me', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    return response.data;
  } catch (error) {
    console.error('Get user error:', error);
    throw extractErrorMessage(error);
  }
};

// Logout user
export const logout = () => {
  localStorage.removeItem('token');
}; 