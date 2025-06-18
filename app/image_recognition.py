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
import base64
import json
from typing import Dict, Tuple, List
from PIL import Image
import numpy as np
from PIL import Image
import requests

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Use OpenAI API instead of CLIP
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI()  # Uses OPENAI_API_KEY environment variable

# Load configuration from config.yaml relative to project root
CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config.yaml')
def load_config():
    with open(CONFIG_PATH, 'r') as f:
        return yaml.safe_load(f)
CONFIG = load_config()
IMGREC_CONFIG = CONFIG.get('image_recognition', {})
POINTS_CONFIG = CONFIG.get('challenge', {}).get('points', {})


def analyze_image(image_data: bytes, image_label: str, confidence_threshold: float = None) -> Dict:
    """
    Analyze the submitted image using OpenAI's Vision API to determine if it matches the target object.
    """
    threshold = confidence_threshold
    if threshold is None:
        threshold = IMGREC_CONFIG.get('confidence_threshold', 0.7)

    print(f"Image label: {image_label}")
    
    # Convert image data to base64 for OpenAI API
    base64_image = base64.b64encode(image_data).decode('utf-8')
    
    # Create a detailed prompt for zero-shot classification
    prompt = f"""
    Please analyze this image and determine if it contains a {image_label}.
    
    Respond with a JSON object containing:
    1. "is_match": true if the image clearly shows a {image_label}, false otherwise
    2. "confidence": a decimal between 0.0 and 1.0 indicating how confident you are
    3. "reasoning": a brief explanation of what you see and why you made this determination
    4. "primary_object": what the main object in the image appears to be
    
    Be strict in your evaluation - only return true if you're confident the image shows a {image_label}.
    Consider lighting, angle, clarity, and whether the object is the main focus of the image.
    
    Example response:
    {{
        "is_match": true,
        "confidence": 0.85,
        "reasoning": "The image clearly shows a [object] in good lighting with clear details visible",
        "primary_object": "{image_label}"
    }}
    """
    
    try:
        # Call OpenAI Vision API
        response = client.chat.completions.create(
            model="gpt-4o",  # Use gpt-4o which has vision capabilities
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                                "detail": "low"
                            }
                        }
                    ]
                }
            ],
            max_tokens=300,
            temperature=0.1  # Low temperature for more consistent results
        )
        
        # Parse the response
        response_text = response.choices[0].message.content
        print(f"OpenAI response: {response_text}")
        
        # Try to extract JSON from the response
        try:
            # Find JSON object in the response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            if start_idx != -1 and end_idx != 0:
                json_str = response_text[start_idx:end_idx]
                analysis_result = json.loads(json_str)
            else:
                raise ValueError("No JSON found in response")
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Failed to parse JSON response: {e}")
            # Fallback: try to extract key information using simple parsing
            is_match = "true" in response_text.lower() and ("is_match" in response_text.lower())
            confidence = 0.5  # Default confidence if we can't parse
            reasoning = response_text[:200] + "..." if len(response_text) > 200 else response_text
            primary_object = "unknown"
            
            analysis_result = {
                "is_match": is_match,
                "confidence": confidence,
                "reasoning": reasoning,
                "primary_object": primary_object
            }
        
        # Extract values with defaults
        is_match = analysis_result.get("is_match", False)
        api_confidence = analysis_result.get("confidence", 0.5)
        reasoning = analysis_result.get("reasoning", "Analysis completed")
        primary_object = analysis_result.get("primary_object", "unknown")
        
        print(f"API confidence: {api_confidence}")
        print(f"Reasoning: {reasoning}")
        print(f"Primary object detected: {primary_object}")
        
        # Apply threshold
        is_correct = is_match and api_confidence > threshold
        
        # Generate user-friendly message
        if is_correct:
            message = f"Great job! That looks like the right item! (Confidence: {api_confidence:.2f})"
        else:
            if not is_match:
                if primary_object != "unknown" and primary_object.lower() != image_label.lower():
                    message = f"This looks more like a {primary_object} than a {image_label}. Try again!"
                else:
                    message = f"I'm not confident this is a {image_label}. Try again!"
            else:
                message = f"The image might show a {image_label}, but I'm not confident enough. Try again! (Confidence: {api_confidence:.2f})"
        
        return {
            "is_match": is_correct,
            "confidence": api_confidence,
            "message": message,
            "debug_info": {
                "api_is_match": is_match,
                "api_confidence": api_confidence,
                "reasoning": reasoning,
                "primary_object": primary_object,
                "threshold_used": threshold
            }
        }
        
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        # Fallback to a safe response
        return {
            "is_match": False,
            "confidence": 0.0,
            "message": f"Unable to analyze image due to technical error. Please try again.",
            "debug_info": {
                "error": str(e),
                "threshold_used": threshold
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


