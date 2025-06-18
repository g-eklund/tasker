#!/usr/bin/env python3
"""
Test script for the image recognition function.
Tests the analyze_image function on random JPEG photos from the validation folder.
"""

import os
import sys
import random
import csv
from pathlib import Path

# Add the parent directory to sys.path so we can import from the app module
sys.path.append(str(Path(__file__).parent.parent))

from app.image_recognition import analyze_image

def load_validation_data():
    """Load the validation CSV file to get photo labels."""
    validation_csv = Path(__file__).parent / "validation.csv"
    validation_data = {}
    
    with open(validation_csv, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            filename = row['filename'].strip()
            object_name = row['name'].strip().strip('"')
            validation_data[filename] = object_name
    
    return validation_data

def get_random_test_image():
    """Select a random JPEG image from the validation folder."""
    validation_dir = Path(__file__).parent
    jpeg_files = list(validation_dir.glob("*.jpeg"))
    
    if not jpeg_files:
        raise FileNotFoundError("No JPEG files found in validation folder")
    
    return random.choice(jpeg_files)

def run_test():
    """Run a single test on a random validation image."""
    print("🧪 Testing Image Recognition Function")
    print("=" * 50)
    
    # Load validation data
    try:
        validation_data = load_validation_data()
        print(f"✅ Loaded validation data for {len(validation_data)} images")
    except Exception as e:
        print(f"❌ Error loading validation data: {e}")
        return
    
    # Select random test image
    try:
        test_image_path = get_random_test_image()
        print(f"🎯 Selected test image: {test_image_path.name}")
    except Exception as e:
        print(f"❌ Error selecting test image: {e}")
        return
    
    # Get expected label
    expected_label = validation_data.get(test_image_path.name)
    if not expected_label:
        print(f"❌ No validation data found for {test_image_path.name}")
        return
    
    print(f"🏷️  Expected object: {expected_label}")
    
    # Load image data
    try:
        with open(test_image_path, 'rb') as f:
            image_data = f.read()
        print(f"📸 Loaded image data: {len(image_data)} bytes")
    except Exception as e:
        print(f"❌ Error loading image: {e}")
        return
    
    # Test the analyze_image function
    print("\n🔍 Analyzing image with OpenAI Vision API...")
    print("-" * 30)
    
    try:
        result = analyze_image(image_data, expected_label)
        
        # Display results
        print(f"✨ Analysis Complete!")
        print(f"   Match: {'✅ YES' if result['is_match'] else '❌ NO'}")
        print(f"   Confidence: {result['confidence']:.3f}")
        print(f"   Message: {result['message']}")
        
        if 'debug_info' in result:
            debug = result['debug_info']
            print(f"\n📊 Debug Information:")
            if 'reasoning' in debug:
                print(f"   Reasoning: {debug['reasoning']}")
            if 'primary_object' in debug:
                print(f"   Detected Object: {debug['primary_object']}")
            if 'api_is_match' in debug:
                print(f"   API Raw Match: {debug['api_is_match']}")
            if 'threshold_used' in debug:
                print(f"   Threshold Used: {debug['threshold_used']}")
        
        # Test summary
        print(f"\n📋 Test Summary:")
        print(f"   Expected: {expected_label}")
        print(f"   Result: {'PASS ✅' if result['is_match'] else 'FAIL ❌'}")
        
        if result['is_match']:
            print(f"   🎉 The AI correctly identified the {expected_label}!")
        else:
            print(f"   🤔 The AI did not confidently identify the {expected_label}")
        
    except Exception as e:
        print(f"❌ Error during image analysis: {e}")
        if "OPENAI_API_KEY" in str(e) or "api" in str(e).lower():
            print("💡 Hint: Make sure your OPENAI_API_KEY environment variable is set")

def run_multiple_tests(num_tests=3):
    """Run multiple tests on random images."""
    print(f"🧪 Running {num_tests} Random Tests")
    print("=" * 60)
    
    results = []
    for i in range(num_tests):
        print(f"\n🔬 Test {i+1}/{num_tests}")
        print("-" * 20)
        
        # We'll modify run_test to return results for batch testing
        try:
            validation_data = load_validation_data()
            test_image_path = get_random_test_image()
            expected_label = validation_data.get(test_image_path.name)
            
            if not expected_label:
                print(f"❌ No validation data for {test_image_path.name}")
                continue
            
            with open(test_image_path, 'rb') as f:
                image_data = f.read()
            
            print(f"Testing: {test_image_path.name} -> {expected_label}")
            result = analyze_image(image_data, expected_label)
            
            test_result = {
                'filename': test_image_path.name,
                'expected': expected_label,
                'is_match': result['is_match'],
                'confidence': result['confidence'],
                'message': result['message']
            }
            results.append(test_result)
            
            print(f"Result: {'PASS ✅' if result['is_match'] else 'FAIL ❌'} (confidence: {result['confidence']:.3f})")
            
        except Exception as e:
            print(f"❌ Test {i+1} failed: {e}")
    
    # Summary
    if results:
        passed = sum(1 for r in results if r['is_match'])
        print(f"\n📊 Batch Test Results:")
        print(f"   Total Tests: {len(results)}")
        print(f"   Passed: {passed}")
        print(f"   Failed: {len(results) - passed}")
        print(f"   Success Rate: {passed/len(results)*100:.1f}%")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test image recognition function")
    parser.add_argument("--batch", type=int, help="Run multiple tests (specify number)")
    parser.add_argument("--single", action="store_true", help="Run a single test (default)")
    
    args = parser.parse_args()
    
    if args.batch:
        run_multiple_tests(args.batch)
    else:
        run_test() 