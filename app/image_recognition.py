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
from typing import Dict, Tuple, List
from PIL import Image

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

def analyze_image(image_data: bytes, target_item_id: int) -> Dict:
    """
    Analyze the submitted image and check if it matches the target item.
    
    In a real implementation, this would call an external API or use a
    machine learning model to recognize objects in the image.
    
    Args:
        image_data: The binary image data
        target_item_id: The ID of the item to look for
        
    Returns:
        A dictionary with analysis results
    """
    # For demonstration purposes, we'll simulate image recognition
    # with a bias toward success (70% chance)
    is_correct = random.random() < 0.7
    
    # In a real implementation, we would:
    # 1. Send the image to a vision API
    # 2. Get back labels/objects detected in the image
    # 3. Compare with our expected item
    
    # Simulate confidence scores for different objects in the image
    detected_objects = {}
    
    if is_correct:
        # Simulate finding the correct item with high confidence
        keywords = ITEM_KEYWORDS.get(target_item_id, [])
        # Choose 2-3 keywords from the list with high confidence
        for keyword in random.sample(keywords, min(3, len(keywords))):
            detected_objects[keyword] = random.uniform(0.7, 0.95)
        
        # Add some random other objects with lower confidence
        for _ in range(3):
            random_item = random.choice(["background", "wall", "floor", "person", "hand", "furniture"])
            detected_objects[random_item] = random.uniform(0.1, 0.5)
    else:
        # Simulate finding incorrect items
        # Maybe add one keyword from the correct item but with low confidence
        keywords = ITEM_KEYWORDS.get(target_item_id, [])
        if keywords:
            detected_objects[random.choice(keywords)] = random.uniform(0.1, 0.4)
        
        # Add other random objects with higher confidence
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
    
    Args:
        time_taken: Time taken to find the item (in seconds)
        max_time: Maximum allowed time for the challenge
        
    Returns:
        Points earned (10-20 points depending on speed)
    """
    # Base points
    base_points = 10
    
    # Bonus points for speed (up to 10 extra points)
    time_ratio = 1 - (time_taken / max_time)
    speed_bonus = round(time_ratio * 10)
    
    return base_points + speed_bonus