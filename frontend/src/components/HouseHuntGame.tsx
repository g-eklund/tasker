import React from 'react';
import { Box, Container, VStack } from '@chakra-ui/react';
import { useGameState } from '../hooks/useGameState';
import PointsDisplay from './PointsDisplay';
import StartScreen from './StartScreen';
import ChallengeScreen from './ChallengeScreen';
import ResultScreen from './ResultScreen';
import CompletionScreen from './CompletionScreen';

const HouseHuntGame: React.FC = () => {
  const {
    gameState,
    gameConfig,
    startNewChallenge,
    submitPhoto,
    resetGame,
    resetSession
  } = useGameState();

  const renderCurrentScreen = () => {
    if (gameState.isComplete) {
      return (
        <CompletionScreen 
          totalPoints={gameState.totalPoints}
          maxPoints={gameConfig.maxPoints}
          averageDuration={gameState.averageDuration}
          onPlayAgain={resetSession} 
        />
      );
    }

    if (gameState.currentChallenge && gameState.isActive) {
      return (
        <ChallengeScreen 
          challenge={gameState.currentChallenge}
          timeRemaining={gameState.timeRemaining}
          onSubmitPhoto={submitPhoto}
          feedback={gameState.feedback}
          feedbackType={gameState.feedbackType}
          onStartOver={resetGame}
        />
      );
    }

    if (gameState.currentChallenge && !gameState.isActive && gameState.feedback) {
      return (
        <ResultScreen 
          feedback={gameState.feedback}
          feedbackType={gameState.feedbackType}
          onPlayAgain={startNewChallenge}
        />
      );
    }

    return (
      <StartScreen 
        totalPoints={gameState.totalPoints}
        maxPoints={gameConfig.maxPoints}
        onStartChallenge={startNewChallenge}
        isLoading={gameState.isLoading}
      />
    );
  };

  return (
    <Box minH="100vh" bg="background" position="relative">
      <PointsDisplay 
        totalPoints={gameState.totalPoints}
        maxPoints={gameConfig.maxPoints}
        averageDuration={gameState.averageDuration}
      />
      <Container maxW="4xl" centerContent py={8}>
        <VStack gap={6} w="full">
          <Box
            bg="white"
            borderRadius="20px"
            boxShadow="0 8px 32px rgba(0, 0, 0, 0.1)"
            p={8}
            w="full"
            textAlign="center"
          >
            {renderCurrentScreen()}
          </Box>
        </VStack>
      </Container>
    </Box>
  );
};

export default HouseHuntGame; 