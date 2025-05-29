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
import numpy as np
from PIL import Image
import requests

from transformers import CLIPProcessor, CLIPModel

model = CLIPModel.from_pretrained("openai/clip-vit-large-patch14")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14")



# Load configuration from config.yaml relative to project root
CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config.yaml')
def load_config():
    with open(CONFIG_PATH, 'r') as f:
        return yaml.safe_load(f)
CONFIG = load_config()
IMGREC_CONFIG = CONFIG.get('image_recognition', {})
POINTS_CONFIG = CONFIG.get('challenge', {}).get('points', {})


def sigmoid(logits):
    return 1 / (1 + np.exp(-logits))


def analyze_image(image_data: bytes, image_label: str, confidence_threshold: float = None) -> Dict:
    """
    Analyze the submitted image using comparative ranking against common household objects.
    More linear and interpretable than absolute confidence scoring.
    """
    threshold = confidence_threshold
    if threshold is None:
        threshold = IMGREC_CONFIG.get('confidence_threshold', 0.7)

    print(f"Image label: {image_label}")
    # Load the image from the bytes data
    image = Image.open(io.BytesIO(image_data))

    # Create a comparative set: target object vs common household items
    # This forces CLIP to make relative comparisons rather than absolute judgments
    comparative_prompts = [
        f"a {image_label}",  # Target object (index 0)
        "a light switch",
        "a door handle", 
        "a wall outlet",
        "a microwave",
        "a pillow",
        "a coffee mug",
        "a mirror",
        "a toothbrush",
        "a computer mouse",
        "a piece of furniture",
        "a kitchen appliance",
        "a bathroom fixture",
        "household decoration",
        "electronic device",
        "home interior item",
        "random household object",
        "wall or ceiling surface",
    ]
    
    # Also test with more specific variants of the target
    target_variants = [
        f"a clear photo of a {image_label}",
        f"a {image_label} in this image", 
        f"this is a {image_label}",
    ]
    
    # Combine all prompts
    all_prompts = comparative_prompts + target_variants

    # Process the image with CLIP
    inputs = processor(
        text=all_prompts,
        images=image,
        return_tensors="pt",
        padding=True
    )

    # Get the logits per image  
    outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image
    
    # Use minimal temperature to get cleaner probabilities
    temperature = 1.0  # No temperature scaling
    probs = logits_per_image.softmax(dim=1)
    
    # Get probabilities
    target_prob = float(probs[0, 0].detach().numpy())  # First prompt is target
    
    # Get max probability among household objects (indices 1-11)
    household_probs = probs[0, 1:12]  # household objects
    max_household_prob = float(household_probs.max().detach().numpy())
    
    # Get max probability among target variants (indices 12+)
    variant_probs = probs[0, 12:]  # target variants
    max_variant_prob = float(variant_probs.max().detach().numpy())
    
    # Combined target confidence (average of direct target and best variant)
    combined_target_conf = (target_prob + max_variant_prob) / 2
    
    # Relative confidence: how much more likely is target vs household objects
    relative_confidence = combined_target_conf / (max_household_prob + combined_target_conf + 1e-8)
    
    # Linear scaling: if target is clearly winning, confidence is high
    # If household objects are winning, confidence is low
    confidence = relative_confidence
    
    print(f"Target probability: {target_prob}")
    print(f"Max variant probability: {max_variant_prob}")
    print(f"Combined target confidence: {combined_target_conf}")
    print(f"Max household object probability: {max_household_prob}")
    print(f"Relative confidence: {relative_confidence}")
    print(f"Final confidence: {confidence}")
    
    is_correct = confidence > threshold
    
    if is_correct:
        message = f"Great job! That looks like the right item! (Confidence: {confidence:.2f})"
    else:
        if max_household_prob > combined_target_conf:
            # Find which household object won
            winning_idx = int(household_probs.argmax()) + 1
            household_objects = [
                "light switch", "door handle", "wall outlet", "microwave", 
                "pillow", "coffee mug", "mirror", "toothbrush", "computer mouse",
                "piece of furniture", "kitchen appliance", "bathroom fixture", 
                "household decoration", "electronic device", "home interior item", 
                "random household object", "wall or ceiling surface"
            ]
            winning_object = household_objects[winning_idx - 1]
            message = f"This looks more like a {winning_object} than a {image_label}. Try again!"
        else:
            message = f"I'm not confident this is a {image_label}. Try again! (Confidence: {confidence:.2f})"
    
    return {
        "is_match": is_correct,
        "confidence": confidence,
        "message": message,
        "debug_info": {
            "target_probability": target_prob,
            "max_variant_probability": max_variant_prob,
            "combined_target_confidence": combined_target_conf,
            "max_household_probability": max_household_prob,
            "relative_confidence": relative_confidence
        }
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


