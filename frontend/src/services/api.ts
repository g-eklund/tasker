import axios from 'axios';
import { Challenge, ChallengeResult } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true, // Important for cookie-based sessions
});

export const gameApi = {
  // Start a new challenge
  startNewChallenge: async (): Promise<Challenge> => {
    console.log('API Base URL:', API_BASE_URL);
    console.log('Starting new challenge...');
    try {
      const response = await api.post('/api/new-challenge');
      console.log('Challenge response:', response.data);
      console.log('Response status:', response.status);
      console.log('Response headers:', response.headers);
      return response.data;
    } catch (error) {
      console.error('API Error in startNewChallenge:', error);
      if (axios.isAxiosError(error)) {
        console.error('Axios error details:', {
          message: error.message,
          status: error.response?.status,
          data: error.response?.data,
          headers: error.response?.headers
        });
      }
      throw error;
    }
  },

  // Submit a photo for the current challenge
  submitPhoto: async (challengeId: string, photoBlob: Blob): Promise<ChallengeResult> => {
    const formData = new FormData();
    formData.append('photo', photoBlob, 'photo.jpg');
    
    const response = await api.post(`/api/submit-photo/${challengeId}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // Get challenge status
  getChallengeStatus: async (challengeId: string) => {
    const response = await api.get(`/api/challenge-status/${challengeId}`);
    return response.data;
  },

  // Get game statistics
  getStats: async () => {
    const response = await api.get('/api/stats');
    return response.data;
  },

  // Get session statistics (average duration, etc.)
  getSessionStats: async (sessionId: string) => {
    const response = await api.get(`/api/session-stats/${sessionId}`);
    return response.data;
  },
};

export default api; 