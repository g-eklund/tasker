import { useState, useEffect, useCallback } from 'react';
import { GameState, ChallengeResult, GameConfig, SessionStats } from '../types';
import { gameApi } from '../services/api';

const INITIAL_GAME_STATE: GameState = {
  totalPoints: 0,
  currentChallenge: null,
  timeRemaining: 0,
  isActive: false,
  isComplete: false,
  feedback: '',
  feedbackType: 'info',
  sessionId: null,
  averageDuration: 0,
};

// Add loading state
interface ExtendedGameState extends GameState {
  isLoading: boolean;
}

const GAME_CONFIG: GameConfig = {
  challengeDuration: 60,
  maxPoints: 100,
  maxPointsPerChallenge: 25,
};

export const useGameState = () => {
  const [gameState, setGameState] = useState<ExtendedGameState>(() => {
    // Load total points from localStorage
    const savedPoints = localStorage.getItem('totalSessionPoints');
    return {
      ...INITIAL_GAME_STATE,
      totalPoints: savedPoints ? parseInt(savedPoints, 10) : 0,
      isLoading: false,
    };
  });



  // Save total points to localStorage whenever it changes
  useEffect(() => {
    localStorage.setItem('totalSessionPoints', gameState.totalPoints.toString());
  }, [gameState.totalPoints]);

  // Timer effect
  useEffect(() => {
    let interval: NodeJS.Timeout | null = null;
    
    if (gameState.isActive && gameState.timeRemaining > 0) {
      interval = setInterval(() => {
        setGameState(prev => ({
          ...prev,
          timeRemaining: Math.max(0, prev.timeRemaining - 1),
        }));
      }, 1000);
    }
    
    return () => {
      if (interval) {
        clearInterval(interval);
      }
    };
  }, [gameState.isActive, gameState.timeRemaining]);

  // Handle time expiration
  useEffect(() => {
    if (gameState.isActive && gameState.timeRemaining === 0) {
      setGameState(prev => ({
        ...prev,
        isActive: false,
        feedback: 'Time\'s up! Try again!',
        feedbackType: 'error',
      }));
    }
  }, [gameState.timeRemaining, gameState.isActive]);

  const startNewChallenge = useCallback(async () => {
    // Prevent multiple simultaneous requests
    if (gameState.isLoading) {
      console.log('useGameState: Already loading, ignoring request');
      return;
    }

    try {
      console.log('useGameState: Starting new challenge...');
      setGameState(prev => ({
        ...prev,
        isLoading: true,
        feedback: 'Starting new challenge...',
        feedbackType: 'info',
      }));

      const challenge = await gameApi.startNewChallenge();
      console.log('useGameState: Received challenge:', challenge);
      
      setGameState(prev => ({
        ...prev,
        isLoading: false,
        currentChallenge: challenge,
        timeRemaining: challenge.time_limit,
        isActive: true,
        feedback: `Find the ${challenge.item.name}!`,
        feedbackType: 'info',
        sessionId: challenge.session_id,
      }));
      console.log('useGameState: State updated successfully');
    } catch (error) {
      console.error('useGameState: Error starting challenge:', error);
      setGameState(prev => ({
        ...prev,
        isLoading: false,
        feedback: 'Failed to start challenge. Please try again.',
        feedbackType: 'error',
      }));
    }
  }, [gameState.isLoading]);

  const fetchSessionStats = useCallback(async (sessionId: string) => {
    try {
      const stats: SessionStats = await gameApi.getSessionStats(sessionId);
      setGameState(prev => ({
        ...prev,
        averageDuration: stats.average_duration,
      }));
    } catch (error) {
      // Silently fail - stats are not critical
    }
  }, []);

  const submitPhoto = useCallback(async (photoBlob: Blob) => {
    if (!gameState.currentChallenge) return;

    try {
      setGameState(prev => ({
        ...prev,
        feedback: 'Analyzing photo...',
        feedbackType: 'info',
      }));

      const result: ChallengeResult = await gameApi.submitPhoto(
        gameState.currentChallenge.challenge_id,
        photoBlob
      );

      if (result.status === 'success') {
        const newTotalPoints = gameState.totalPoints + (result.points || 0);
        const isGameComplete = newTotalPoints >= GAME_CONFIG.maxPoints;

        setGameState(prev => ({
          ...prev,
          totalPoints: newTotalPoints,
          isActive: false,
          isComplete: isGameComplete,
          feedback: result.message,
          feedbackType: 'success',
        }));

        // Fetch updated session stats after successful challenge
        if (gameState.sessionId) {
          fetchSessionStats(gameState.sessionId);
        }
      } else {
        setGameState(prev => ({
          ...prev,
          feedback: result.message,
          feedbackType: 'error',
          isActive: !result.completed,
        }));
      }
    } catch (error) {
      setGameState(prev => ({
        ...prev,
        feedback: 'Failed to submit photo. Please try again.',
        feedbackType: 'error',
      }));
    }
  }, [gameState.currentChallenge, gameState.totalPoints, gameState.sessionId, fetchSessionStats]);

  const resetGame = useCallback(() => {
    // Reset everything including total points and localStorage
    localStorage.removeItem('totalSessionPoints');
    setGameState({
      ...INITIAL_GAME_STATE,
      isLoading: false,
    });
  }, []);

  const resetSession = useCallback(() => {
    // This is the same as resetGame now, but kept for semantic clarity
    localStorage.removeItem('totalSessionPoints');
    setGameState({
      ...INITIAL_GAME_STATE,
      isLoading: false,
    });
  }, []);

  return {
    gameState,
    gameConfig: GAME_CONFIG,
    startNewChallenge,
    submitPhoto,
    resetGame,
    resetSession,
  };
}; 