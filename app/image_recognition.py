"""
Image recognition module for the House Hunt Challenge app.

This module provides functionality to compare user-submitted photos
with challenge items to determine if they match.

In a production version, this would integrate with a proper image 
recognition API like Google Cloud Vision, Azure Computer Vision, 
or use a pre-trained model with TensorFlow/PyTorch.

For now, we'll implement a simple simulated version.
"""

import io
import random
import yaml
import os
from typing import Dict, Tuple, List
from PIL import Image

# Load configuration from config.yaml relative to project root
CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config.yaml')
def load_config():
    with open(CONFIG_PATH, 'r') as f:
        return yaml.safe_load(f)
CONFIG = load_config()
IMGREC_CONFIG = CONFIG.get('image_recognition', {})
POINTS_CONFIG = CONFIG.get('challenge', {}).get('points', {})

# Map of item IDs to their expected keywords
# In a real implementation, these would be labels returned by an image recognition API
ITEM_KEYWORDS = {
    1: ["toilet", "paper", "roll", "bathroom", "tissue"],
    2: ["shower", "head", "bathroom", "water"],
    3: ["sofa", "couch", "furniture", "living room", "seat"],
    4: ["tv", "television", "screen", "monitor", "living room"],
    5: ["door", "entrance", "exit", "front door", "wooden"],
    6: ["sink", "faucet", "tap", "kitchen", "water"],
    7: ["light", "switch", "wall", "electricity", "button"],
    8: ["plant", "green", "leaf", "pot", "nature"]
}

def analyze_image(image_data: bytes, target_item_id: int, confidence_threshold: float = None) -> Dict:
    """
    Analyze the submitted image and check if it matches the target item.
    Loads default thresholds from config.yaml if not explicitly provided.
    """
    threshold = confidence_threshold
    if threshold is None:
        threshold = IMGREC_CONFIG.get('confidence_threshold', 0.7)
    max_objects = IMGREC_CONFIG.get('max_objects', 5)
    # For demonstration purposes, we'll simulate image recognition
    # with a bias toward success (default: config threshold)
    is_correct = random.random() < threshold
    # Simulate confidence scores for different objects in the image
    detected_objects = {}
    
    if is_correct:
        keywords = ITEM_KEYWORDS.get(target_item_id, [])
        # Choose up to max_objects keywords from the list with high confidence
        for keyword in random.sample(keywords, min(max_objects, len(keywords))):
            detected_objects[keyword] = random.uniform(0.7, 0.95)
        # Add some random other objects with lower confidence
        for _ in range(3):
            random_item = random.choice(["background", "wall", "floor", "person", "hand", "furniture"])
            detected_objects[random_item] = random.uniform(0.1, 0.5)
    else:
        keywords = ITEM_KEYWORDS.get(target_item_id, [])
        if keywords:
            detected_objects[random.choice(keywords)] = random.uniform(0.1, 0.4)
        for _ in range(4):
            random_item = random.choice(["background", "wall", "floor", "person", "hand", "furniture", "device"])
            detected_objects[random_item] = random.uniform(0.5, 0.9)
    # Determine match based on our simulation
    if is_correct:
        match_confidence = random.uniform(0.7, 0.95)
        message = "Great job! That looks like the right item!"
    else:
        match_confidence = random.uniform(0.1, 0.4)
        message = "That doesn't look like the right item. Try again!"
    return {
        "is_match": is_correct,
        "confidence": match_confidence,
        "detected_objects": detected_objects,
        "message": message
    }

def get_points_for_match(time_taken: float, max_time: float) -> int:
    """
    Calculate points based on how quickly the item was found.
    Uses configuration from config.yaml if available.
    """
    base_points = POINTS_CONFIG.get('base', 10)
    # If not explicitly set, fall back to 10
    time_multiplier = POINTS_CONFIG.get('time_multiplier', 1)
    # Bonus points for speed (optionally scaled by config time_multiplier)
    time_ratio = 1 - (time_taken / max_time)
    speed_bonus = round(time_ratio * 10 * time_multiplier)
    return base_points + speed_bonus