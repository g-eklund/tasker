import React from 'react';
import {
  VStack,
  Button,
  Text,
  Box,
  Heading,
  HStack,
} from '@chakra-ui/react';

interface CompletionScreenProps {
  totalPoints: number;
  maxPoints: number;
  averageDuration: number;
  onPlayAgain: () => void;
}

const CompletionScreen: React.FC<CompletionScreenProps> = ({
  totalPoints,
  maxPoints,
  averageDuration,
  onPlayAgain,
}) => {
  return (
    <VStack gap={6}>
      <Box
        bg="gradient-to-r from-yellow.200 to-orange.200"
        p={8}
        borderRadius="25px"
        textAlign="center"
        border="3px solid"
        borderColor="yellow.400"
        boxShadow="0 12px 30px rgba(255, 193, 7, 0.3)"
      >
        <Text fontSize="8xl" mb={4}>
          🏆
        </Text>
        <Heading size="2xl" color="yellow.700" mb={4}>
          Congratulations!
        </Heading>
        <Text fontSize="xl" color="yellow.600" fontWeight="bold" mb={4}>
          You completed the House Hunt Challenge!
        </Text>
        
        <HStack justify="center" gap={4} mb={4}>
          <Box
            bg="yellow.400"
            color="yellow.900"
            px={4}
            py={2}
            borderRadius="full"
            fontWeight="bold"
          >
            🌟 {totalPoints} Points
          </Box>
          <Box
            bg="orange.400"
            color="orange.900"
            px={4}
            py={2}
            borderRadius="full"
            fontWeight="bold"
          >
            🎯 Goal Reached!
          </Box>
        </HStack>

        {averageDuration > 0 && (
          <Box
            bg="purple.100"
            p={4}
            borderRadius="15px"
            border="2px solid"
            borderColor="purple.300"
            mb={4}
          >
            <Text fontSize="lg" fontWeight="bold" color="purple.700" textAlign="center">
              ⚡ Your Average Speed: {averageDuration} seconds
            </Text>
            <Text fontSize="sm" color="purple.600" textAlign="center" mt={1}>
              Challenge your friends to beat this time! 🏃‍♂️💨
            </Text>
          </Box>
        )}

        <Text fontSize="lg" color="yellow.600">
          You're a master house hunter! 🕵️‍♀️
        </Text>
      </Box>

      <VStack gap={4}>
        <Button
          size="lg"
          colorScheme="yellow"
          onClick={onPlayAgain}
          fontSize="xl"
          h="60px"
          px={8}
          borderRadius="30px"
          boxShadow="0 6px 15px rgba(255, 193, 7, 0.3)"
          _hover={{
            transform: 'scale(1.05)',
            boxShadow: '0 8px 20px rgba(255, 193, 7, 0.4)',
          }}
          _active={{
            transform: 'scale(0.98)',
          }}
          transition="all 0.2s ease"
        >
          🎮 Play Again!
        </Button>

        <Text fontSize="sm" color="gray.500" textAlign="center">
          Challenge your friends and family to beat your score!
        </Text>
      </VStack>
    </VStack>
  );
};

export default CompletionScreen; 