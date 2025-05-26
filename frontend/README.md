# House Hunt Challenge - React Frontend

A modern, kid-friendly React frontend for the House Hunt Challenge game built with Chakra UI.

## Features

- 🎨 **Kid-Friendly Design**: Bright colors, fun fonts (Comic Sans MS), and emoji-rich interface
- 📱 **Responsive**: Works on desktop, tablet, and mobile devices
- 📸 **Camera Integration**: Uses react-webcam for photo capture
- 🎯 **Real-time Feedback**: Instant feedback on photo submissions
- 🏆 **Progress Tracking**: Visual progress bars and point tracking
- ⏰ **Timer**: Countdown timer for each challenge

## Tech Stack

- **React 18** with TypeScript
- **Chakra UI** for components and styling
- **React Webcam** for camera functionality
- **Axios** for API communication
- **Framer Motion** for animations (via Chakra UI)

## Getting Started

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm start
   ```

3. Make sure the FastAPI backend is running on `http://localhost:8000`

## Components

- **HouseHuntGame**: Main game component that manages state
- **StartScreen**: Welcome screen with start button
- **ChallengeScreen**: Active challenge with camera and timer
- **ResultScreen**: Shows feedback after photo submission
- **CompletionScreen**: Celebration screen when goal is reached
- **PointsDisplay**: Fixed position points counter

## API Integration

The frontend communicates with the FastAPI backend through:
- `POST /api/new-challenge` - Start a new challenge
- `POST /api/submit-photo/{challenge_id}` - Submit a photo
- `GET /api/challenge-status/{challenge_id}` - Get challenge status
- `GET /api/stats` - Get game statistics

## Customization

The theme can be customized in `src/App.tsx`. The current theme features:
- Primary colors: Purple/Indigo palette
- Secondary colors: Blue palette  
- Accent colors: Orange palette
- Kid-friendly fonts: Comic Sans MS
- Rounded corners and soft shadows throughout
