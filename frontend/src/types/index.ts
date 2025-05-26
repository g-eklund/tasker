export interface ChallengeItem {
  id: number;
  name: string;
  image: string;
  difficulty: 'easy' | 'medium' | 'hard';
}

export interface Challenge {
  challenge_id: string;
  item: ChallengeItem;
  time_limit: number;
  start_time: number;
  session_id: string;
}

export interface ChallengeResult {
  status: 'success' | 'failed';
  message: string;
  points?: number;
  completed: boolean;
  confidence?: number;
  detected_objects?: string[];
}

export interface GameState {
  totalPoints: number;
  currentChallenge: Challenge | null;
  timeRemaining: number;
  isActive: boolean;
  isComplete: boolean;
  feedback: string;
  feedbackType: 'success' | 'error' | 'info';
  sessionId: string | null;
  averageDuration: number;
}

export interface GameConfig {
  challengeDuration: number;
  maxPoints: number;
  maxPointsPerChallenge: number;
}

export interface SessionStats {
  total_successful_challenges: number;
  average_duration: number;
} 