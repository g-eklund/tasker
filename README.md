# 🏠 House Hunt Challenge

A fun, kid-friendly game where players use their camera to find objects around their house! Built with a modern React frontend and FastAPI backend.

## 🎮 Game Overview

The House Hunt Challenge is an interactive game designed for kids that combines technology with physical exploration. Players receive challenges to find specific items around their house and use their device's camera to "capture" these items. The game features:

- **Real-time object detection** using AI image recognition
- **Kid-friendly interface** with bright colors and fun animations
- **Progressive difficulty** with different challenge items
- **Point-based scoring** system with visual progress tracking
- **Time-based challenges** to add excitement

## 🏗️ Architecture

### Frontend (React + Chakra UI)
- **Location**: `./frontend/`
- **Tech Stack**: React 18, TypeScript, Chakra UI, React Webcam
- **Features**: Modern, responsive UI with camera integration
- **Port**: 3000 (development)

### Backend (FastAPI + Python)
- **Location**: `./` (root directory)
- **Tech Stack**: FastAPI, Python, Supabase, OpenAI Vision API
- **Features**: RESTful API, image recognition, session management
- **Port**: 8000

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Supabase account (for data storage)
- OpenAI API key (for image recognition)

### Backend Setup

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables**:
   Create a `.env` file in the root directory:
   ```env
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_anon_key
   OPENAI_API_KEY=your_openai_api_key
   ```

3. **Start the backend server**:
   ```bash
   uvicorn main:app --reload
   ```
   The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start the development server**:
   ```bash
   npm start
   ```
   The app will open at `http://localhost:3000`

## 🎨 Design Philosophy

### Kid-Friendly Features
- **Bright, cheerful colors** with purple, blue, and orange themes
- **Comic Sans MS font** for a playful, approachable feel
- **Large, rounded buttons** that are easy to tap
- **Emoji-rich interface** for visual appeal
- **Clear visual feedback** for all interactions
- **Simple navigation** with minimal complexity

### Accessibility
- **High contrast colors** for better readability
- **Large touch targets** for easier interaction
- **Clear visual hierarchy** with proper heading structure
- **Responsive design** that works on all devices

## 🔧 Configuration

### Game Settings (`config.yaml`)
```yaml
challenge:
  points:
    max_per_challenge: 25
    goal: 100
  time:
    default_duration: 60

content:
  items:
    - id: 1
      name: "Toilet Paper Roll"
      image: "toilet_paper.jpg"
      difficulty: "easy"
    # ... more items
```

### Theme Customization (`frontend/src/App.tsx`)
The Chakra UI theme can be customized with:
- Custom color palettes
- Typography settings
- Component style overrides
- Animation configurations

## 📱 Features

### For Kids
- **Simple gameplay**: Point camera, take photo, get points!
- **Instant feedback**: Know immediately if you found the right item
- **Progress tracking**: See how close you are to winning
- **Celebration animations**: Fun rewards for completing challenges

### For Parents/Educators
- **Safe environment**: No external links or inappropriate content
- **Educational value**: Encourages exploration and observation skills
- **Customizable content**: Easy to add new challenge items
- **Session tracking**: Monitor progress and engagement

## 🔌 API Endpoints

- `POST /api/new-challenge` - Start a new challenge
- `POST /api/submit-photo/{challenge_id}` - Submit a photo for analysis
- `GET /api/challenge-status/{challenge_id}` - Check challenge status
- `GET /api/stats` - Get game statistics

## 🗄️ Database Schema

### Tables (Supabase)
- **sessions**: Track user sessions and total points
- **challenge-events**: Log individual challenge attempts
- **users**: Store user information (optional)

## 🚀 Deployment

### Frontend (Netlify/Vercel)
```bash
cd frontend
npm run build
# Deploy the build/ directory
```

### Backend (Railway/Heroku)
```bash
# Ensure all environment variables are set
# Deploy with your preferred platform
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Chakra UI** for the excellent component library
- **FastAPI** for the fast and modern Python web framework
- **OpenAI** for the powerful vision API
- **Supabase** for the backend-as-a-service platform