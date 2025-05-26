import React from 'react';
import {
  VStack,
  Button,
  Text,
  Box,
  HStack,
  Image,
} from '@chakra-ui/react';

interface StartScreenProps {
  totalPoints: number;
  maxPoints: number;
  onStartChallenge: () => void;
}

const StartScreen: React.FC<StartScreenProps> = ({ 
  totalPoints, 
  maxPoints, 
  onStartChallenge 
}) => {
  const progressPercentage = (totalPoints / maxPoints) * 100;

  return (
    <VStack gap={6}>
      {/* Logo */}
      <Box textAlign="center">
        <Image
          src="/logo512.png"
          alt="House Hunt Challenge Logo"
          maxW="120px"
          maxH="120px"
          mx="auto"
          borderRadius="20px"
          boxShadow="0 4px 15px rgba(0, 0, 0, 0.1)"
          _hover={{
            transform: 'scale(1.05)',
            boxShadow: '0 6px 20px rgba(0, 0, 0, 0.15)',
          }}
          transition="all 0.3s ease"
        />
        <Text 
          fontSize="2xl" 
          fontWeight="bold" 
          color="primary.600" 
          mt={3}
          textAlign="center"
        >
          🏠 House Hunt Challenge 🔍
        </Text>
      </Box>

      {totalPoints > 0 && (
        <Box
          bg="yellow.100"
          p={4}
          borderRadius="15px"
          border="2px solid"
          borderColor="yellow.300"
        >
          <HStack justify="center" gap={2}>
            <Text fontSize="lg">⭐</Text>
            <Text fontSize="lg" fontWeight="bold" color="yellow.700">
              You have {totalPoints} points so far!
            </Text>
            <Text fontSize="lg">⭐</Text>
          </HStack>
          <Text fontSize="sm" color="yellow.600" textAlign="center" mt={1}>
            {progressPercentage.toFixed(0)}% complete
          </Text>
        </Box>
      )}

      <Button
        size="lg"
        colorScheme="primary"
        onClick={onStartChallenge}
        fontSize="2xl"
        h="80px"
        px={12}
        borderRadius="40px"
        boxShadow="0 8px 20px rgba(102, 0, 230, 0.3)"
        _hover={{
          transform: 'scale(1.05)',
          boxShadow: '0 12px 25px rgba(102, 0, 230, 0.4)',
        }}
        _active={{
          transform: 'scale(0.98)',
        }}
        transition="all 0.2s ease"
      >
        🚀 Start New Challenge! 🎯
      </Button>

      <Text fontSize="md" color="gray.600" textAlign="center" maxW="400px">
        Get ready to hunt for objects around your house! 
        Use your camera to find the items as quickly as possible.
      </Text>

      {totalPoints === 0 && (
        <Box
          bg="blue.50"
          p={4}
          borderRadius="15px"
          border="2px solid"
          borderColor="blue.200"
        >
          <Text fontSize="sm" color="blue.700" textAlign="center">
            💡 <strong>Tip:</strong> Make sure you have good lighting and hold your camera steady!
          </Text>
        </Box>
      )}
    </VStack>
  );
};

export default StartScreen; 