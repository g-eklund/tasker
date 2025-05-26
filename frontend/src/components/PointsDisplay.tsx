import React from 'react';
import {
  Box,
  Text,
  VStack,
  HStack,
  Badge,
} from '@chakra-ui/react';

interface PointsDisplayProps {
  totalPoints: number;
  maxPoints: number;
  averageDuration: number;
}

const PointsDisplay: React.FC<PointsDisplayProps> = ({ totalPoints, maxPoints, averageDuration }) => {
  const progressPercentage = (totalPoints / maxPoints) * 100;

  return (
    <Box
      position="fixed"
      top={4}
      right={4}
      bg="primary.600"
      color="white"
      p={4}
      borderRadius="20px"
      boxShadow="0 4px 12px rgba(0, 0, 0, 0.2)"
      zIndex={100}
      minW="200px"
    >
      <VStack gap={2} align="stretch">
        <HStack justify="space-between">
          <Text fontSize="lg" fontWeight="bold">
            🏆 Points
          </Text>
          <Badge colorScheme="yellow" fontSize="md" px={2} py={1} borderRadius="full">
            {totalPoints}/{maxPoints}
          </Badge>
        </HStack>
        
        <Box
          bg="primary.700"
          borderRadius="full"
          h="8px"
          overflow="hidden"
        >
          <Box
            bg="yellow.400"
            h="full"
            borderRadius="full"
            width={`${progressPercentage}%`}
            transition="width 0.3s ease"
          />
        </Box>
        
        <Text fontSize="sm" textAlign="center" opacity={0.9}>
          {progressPercentage.toFixed(0)}% Complete
        </Text>
        
        {averageDuration > 0 && (
          <Text fontSize="xs" textAlign="center" opacity={0.8} mt={1}>
            ⚡ Avg: {averageDuration}s
          </Text>
        )}
      </VStack>
    </Box>
  );
};

export default PointsDisplay; 