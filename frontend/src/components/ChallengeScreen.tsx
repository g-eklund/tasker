import React, { useRef, useCallback } from 'react';
import {
  VStack,
  Button,
  Text,
  Box,
  Image,
  Heading,
  HStack,
} from '@chakra-ui/react';
import Webcam from 'react-webcam';
import { Challenge } from '../types';

interface ChallengeScreenProps {
  challenge: Challenge;
  timeRemaining: number;
  feedback: string;
  feedbackType: 'success' | 'error' | 'info';
  onSubmitPhoto: (photoBlob: Blob) => void;
  onStartOver: () => void;
}

const ChallengeScreen: React.FC<ChallengeScreenProps> = ({
  challenge,
  timeRemaining,
  feedback,
  feedbackType,
  onSubmitPhoto,
  onStartOver,
}) => {
  const webcamRef = useRef<Webcam>(null);

  const capturePhoto = useCallback(() => {
    const imageSrc = webcamRef.current?.getScreenshot();
    if (imageSrc) {
      // Convert base64 to blob
      fetch(imageSrc)
        .then(res => res.blob())
        .then(blob => onSubmitPhoto(blob));
    }
  }, [onSubmitPhoto]);

  const timePercentage = (timeRemaining / challenge.time_limit) * 100;
  const isTimeRunningOut = timeRemaining <= 10;



  return (
    <VStack gap={6} w="full">
      <Heading size="lg" color="primary.600" textAlign="center">
        🔍 Find this item:
      </Heading>
      
      <Box
        bg="gradient.100"
        p={6}
        borderRadius="20px"
        border="3px solid"
        borderColor="primary.200"
        textAlign="center"
      >
        <Text fontSize="3xl" fontWeight="bold" color="primary.700" mb={4}>
          {challenge.item.name}
        </Text>
        <Image
          src={`/static/images/${challenge.item.image}`}
          alt={challenge.item.name}
          maxH="200px"
          mx="auto"
          borderRadius="15px"
          boxShadow="0 4px 12px rgba(0, 0, 0, 0.2)"
        />
      </Box>

      {/* Timer */}
      <Box textAlign="center">
        <Text
          fontSize="4xl"
          fontWeight="bold"
          color={isTimeRunningOut ? "red.500" : "accent.500"}
          mb={2}
        >
          ⏰ {timeRemaining}s
        </Text>
        <Box
          bg="gray.200"
          borderRadius="full"
          h="12px"
          w="300px"
          mx="auto"
          overflow="hidden"
        >
          <Box
            bg={isTimeRunningOut ? "red.400" : "accent.400"}
            h="full"
            borderRadius="full"
            width={`${timePercentage}%`}
            transition="all 0.3s ease"
          />
        </Box>
      </Box>

      {/* Camera */}
      <Box
        borderRadius="20px"
        overflow="hidden"
        boxShadow="0 8px 20px rgba(0, 0, 0, 0.2)"
        bg="gray.100"
        p={2}
      >
        <Webcam
          ref={webcamRef}
          audio={false}
          screenshotFormat="image/jpeg"
          width={400}
          height={300}
          style={{ borderRadius: '15px' }}
        />
      </Box>

      <HStack gap={4} justify="center">
        <Button
          size="lg"
          colorScheme="accent"
          onClick={capturePhoto}
          fontSize="xl"
          h="60px"
          px={8}
          borderRadius="30px"
          boxShadow="0 6px 15px rgba(230, 140, 0, 0.3)"
          _hover={{
            transform: 'scale(1.05)',
            boxShadow: '0 8px 20px rgba(230, 140, 0, 0.4)',
          }}
          _active={{
            transform: 'scale(0.98)',
          }}
          transition="all 0.2s ease"
        >
          📸 Take Photo
        </Button>
        
        <Button
          size="md"
          variant="outline"
          colorScheme="gray"
          onClick={onStartOver}
          fontSize="md"
          h="60px"
          px={6}
          borderRadius="30px"
          _hover={{
            transform: 'scale(1.02)',
            bg: 'gray.50',
          }}
          _active={{
            transform: 'scale(0.98)',
          }}
          transition="all 0.2s ease"
        >
          🔄 Start Over
        </Button>
      </HStack>

      {feedback && (
        <Box
          bg={feedbackType === 'success' ? 'green.100' : feedbackType === 'error' ? 'red.100' : 'blue.100'}
          color={feedbackType === 'success' ? 'green.700' : feedbackType === 'error' ? 'red.700' : 'blue.700'}
          p={4}
          borderRadius="15px"
          maxW="400px"
          textAlign="center"
        >
          <Text fontWeight="bold">{feedback}</Text>
        </Box>
      )}
    </VStack>
  );
};

export default ChallengeScreen; 