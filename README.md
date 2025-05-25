# House Hunt Challenge App

A fun web application that gives kids challenges to find and photograph items around the house under time constraints.

## How It Works

1. Kids tap "Start New Challenge" button
2. They receive an image of something commonly found in a house (toilet paper, shower head, sofa, etc.)
3. They have 60 seconds to find and take a photo of that item
4. Our image recognition system verifies if they found the correct item
5. They earn points for successful finds!

## Installation

1. Clone this repository
2. Install dependencies:

```bash
pip install -e .
```

## Running the App

```bash
python main.py
```

Then open your browser to http://localhost:8000

## Features

- Timed challenges (default: 60 seconds)
- Camera integration using device camera
- Simple image recognition (simulated in this version)
- Points system for successful challenges
- Kid-friendly UI with fun animations

## Technical Details

- Backend: FastAPI with Python 3.12+
- Frontend: HTML, CSS, JavaScript (using browser's built-in camera API)
- Image Recognition: Currently simulated; can be integrated with Google Cloud Vision or similar services

## Future Enhancements

- User accounts to save progress
- Different difficulty levels
- Themed challenge packs (kitchen items, bathroom items, etc.)
- Multiplayer mode for competitions between siblings or friends