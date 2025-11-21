import axios from 'axios';

const API_BASE_URL = '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const connectSQLite = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await axios.post(`${API_BASE_URL}/connect/sqlite`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
};

export const connectMySQL = async (credentials) => {
  const response = await api.post('/connect/mysql', credentials);
  return response.data;
};

export const getSchema = async (sessionId) => {
  const response = await api.get(`/schema/${sessionId}`);
  return response.data;
};

export const askQuestion = async (questionData) => {
  const response = await api.post('/ask', questionData);
  return response.data;
};

export const executeQuery = async (queryData) => {
  const response = await api.post('/execute', queryData);
  return response.data;
};

export const visualizeData = async (vizData) => {
  const response = await api.post('/visualize', vizData);
  return response.data;
};

export const getQueryHistory = async (sessionId) => {
  const response = await api.get(`/history/${sessionId}`);
  return response.data;
};

export const closeSession = async (sessionId) => {
  const response = await api.delete(`/session/${sessionId}`);
  return response.data;
};

export default api;
