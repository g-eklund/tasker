import React from 'react';
import {
  VStack,
  Button,
  Text,
  Box,
  Heading,
} from '@chakra-ui/react';

interface ResultScreenProps {
  feedback: string;
  feedbackType: 'success' | 'error' | 'info';
  onPlayAgain: () => void;
}

const ResultScreen: React.FC<ResultScreenProps> = ({
  feedback,
  feedbackType,
  onPlayAgain,
}) => {
  const getEmoji = () => {
    switch (feedbackType) {
      case 'success': return '🎉';
      case 'error': return '😔';
      default: return '🤔';
    }
  };

  const getBgColor = () => {
    switch (feedbackType) {
      case 'success': return 'green.100';
      case 'error': return 'red.100';
      default: return 'blue.100';
    }
  };

  const getTextColor = () => {
    switch (feedbackType) {
      case 'success': return 'green.700';
      case 'error': return 'red.700';
      default: return 'blue.700';
    }
  };

  return (
    <VStack gap={6}>
      <Box
        bg={getBgColor()}
        p={6}
        borderRadius="20px"
        textAlign="center"
        maxW="500px"
      >
        <Text fontSize="6xl" mb={4}>
          {getEmoji()}
        </Text>
        <Heading size="lg" color={getTextColor()} mb={4}>
          {feedbackType === 'success' ? 'Great Job!' : 'Try Again!'}
        </Heading>
        <Text fontSize="lg" color={getTextColor()} fontWeight="bold">
          {feedback}
        </Text>
      </Box>

      <Button
        size="lg"
        colorScheme="primary"
        onClick={onPlayAgain}
        fontSize="xl"
        h="60px"
        px={8}
        borderRadius="30px"
        boxShadow="0 6px 15px rgba(102, 0, 230, 0.3)"
        _hover={{
          transform: 'scale(1.05)',
          boxShadow: '0 8px 20px rgba(102, 0, 230, 0.4)',
        }}
        _active={{
          transform: 'scale(0.98)',
        }}
        transition="all 0.2s ease"
      >
        🎯 Try Another Challenge!
      </Button>
    </VStack>
  );
};

export default ResultScreen; 