#!/usr/bin/env python3
"""
analyze_plant.py - Analyze plant images for health issues
Provides comprehensive plant health analysis using computer vision and machine learning
"""

import argparse
import sys
import os
import json
import sqlite3
import logging
from datetime import datetime
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import cv2
    import numpy as np
    from PIL import Image
    import yaml
except ImportError as e:
    print(f"Error: Required library not installed: {e}")
    print("Run 'scripts/setup.sh' to install dependencies")
    sys.exit(1)

# Load configuration
def load_config():
    """Load configuration from .env file"""
    config = {}

    # Default values
    defaults = {
        'ANALYSIS_MODE': 'standard',
        'LOG_LEVEL': 'info',
        'LOG_FILE': '/var/log/plant-whisperer.log',
        'PLANT_DB_PATH': '/opt/plant-whisperer/plants.db',
        'IMAGE_STORAGE_PATH': '/opt/plant-whisperer/images',
        'AI_DETECTION_ENABLED': 'true',
        'AI_CONFIDENCE_THRESHOLD': '0.75',
        'MIN_IMAGE_WIDTH': '1920',
        'MIN_IMAGE_HEIGHT': '1080',
        'GROWTH_STAGE_ANALYSIS': 'true',
        'NUTRIENT_ANALYSIS': 'true',
        'PEST_DISEASE_ANALYSIS': 'true',
        'ENV_STRESS_ANALYSIS': 'true',
        'PREFERRED_APPROACH': 'organic',
    }

    # Try to load from .env
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    env_file = os.path.join(project_root, '.env')

    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    config[key] = value

    # Apply defaults for missing values
    for key, value in defaults.items():
        if key not in config:
            config[key] = value

    return config

# Setup logging
def setup_logging(config):
    """Setup logging configuration"""
    log_level = getattr(logging, config['LOG_LEVEL'].upper(), logging.INFO)
    log_file = config['LOG_FILE']

    # Create log directory if needed
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )

    return logging.getLogger('plant_whisperer')

# Image preprocessing
def preprocess_image(image_path, config, logger):
    """Preprocess image for analysis"""
    logger.info(f"Loading image: {image_path}")

    # Check if image exists
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    # Load image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not load image: {image_path}")

    # Check image dimensions
    height, width = image.shape[:2]
    min_width = int(config['MIN_IMAGE_WIDTH'])
    min_height = int(config['MIN_IMAGE_HEIGHT'])

    if width < min_width or height < min_height:
        logger.warning(f"Image resolution ({width}x{height}) below recommended ({min_width}x{min_height})")

    # Convert to different color spaces
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Apply CLAHE for contrast enhancement
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    lab_planes = list(cv2.split(lab_image))
    lab_planes[0] = clahe.apply(lab_planes[0])
    enhanced_lab = cv2.merge(lab_planes)
    enhanced_image = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2RGB)

    logger.info(f"Image loaded successfully: {width}x{height}")

    return {
        'original': image,
        'rgb': rgb_image,
        'lab': lab_image,
        'hsv': hsv_image,
        'enhanced': enhanced_image,
        'width': width,
        'height': height
    }

# Color analysis
def analyze_color(images, config, logger):
    """Analyze plant color for health indicators"""
    logger.info("Analyzing color patterns...")

    results = {
        'chlorosis': False,
        'necrosis': False,
        'purpling': False,
        'bronzing': False,
        'color_deviation': 0.0,
        'color_description': ''
    }

    # Analyze LAB color space (better for plant color analysis)
    lab = images['lab']
    l_channel, a_channel, b_channel = cv2.split(lab)

    # Calculate statistics
    l_mean = np.mean(l_channel)
    a_mean = np.mean(a_channel)
    b_mean = np.mean(b_channel)

    # Detect chlorosis (yellowing - high L, high a, high b)
    yellow_mask = cv2.inRange(lab, np.array([100, 120, 120]), np.array([255, 255, 255]))
    yellow_ratio = np.count_nonzero(yellow_mask) / (lab.shape[0] * lab.shape[1])
    results['chlorosis'] = yellow_ratio > 0.2

    # Detect necrosis (dead tissue - low L, low a, low b or very dark)
    dark_mask = cv2.inRange(lab, np.array([0, 110, 110]), np.array([80, 140, 140]))
    dark_ratio = np.count_nonzero(dark_mask) / (lab.shape[0] * lab.shape[1])
    results['necrosis'] = dark_ratio > 0.1

    # Calculate color deviation from healthy green
    # Healthy green in LAB: L=70-100, a=110-130, b=110-130
    healthy_l = 85
    healthy_a = 120
    healthy_b = 120

    l_deviation = abs(l_mean - healthy_l) / healthy_l
    a_deviation = abs(a_mean - healthy_a) / healthy_a
    b_deviation = abs(b_mean - healthy_b) / healthy_b

    results['color_deviation'] = (l_deviation + a_deviation + b_deviation) / 3

    # Generate color description
    if results['chlorosis']:
        results['color_description'] = "Yellowing (chlorosis) detected"
    elif results['necrosis']:
        results['color_description'] = "Dead tissue (necrosis) detected"
    elif results['color_deviation'] > 0.3:
        results['color_description'] = "Significant color deviation from healthy"
    else:
        results['color_description'] = "Color appears healthy"

    logger.info(f"Color analysis: {results['color_description']}")

    return results

# Texture analysis
def analyze_texture(images, config, logger):
    """Analyze leaf texture for abnormalities"""
    logger.info("Analyzing texture patterns...")

    results = {
        'powdery_mildew': False,
        'downy_mildew': False,
        'rust': False,
        'smoothness': 0.0,
        'texture_description': ''
    }

    # Convert to grayscale for texture analysis
    gray = cv2.cvtColor(images['rgb'], cv2.COLOR_RGB2GRAY)

    # Calculate texture features using GLCM
    # This is a simplified version - full GLCM requires more computation
    texture_contrast = np.std(gray) / np.mean(gray)

    # Detect powdery mildew (white powdery coating)
    # In LAB: high L, mid a, mid b
    powdery_mask = cv2.inRange(images['lab'], np.array([180, 110, 110]), np.array([255, 150, 150]))
    powdery_ratio = np.count_nonzero(powdery_mask) / (gray.shape[0] * gray.shape[1])
    results['powdery_mildew'] = powdery_ratio > 0.15

    # Detect rust (orange/brown spots)
    # In RGB: high R, medium G, low B
    rust_mask = cv2.inRange(images['rgb'], np.array([150, 50, 20]), np.array([255, 150, 80]))
    rust_ratio = np.count_nonzero(rust_mask) / (gray.shape[0] * gray.shape[1])
    results['rust'] = rust_ratio > 0.1

    results['smoothness'] = 1.0 - min(texture_contrast, 1.0)

    # Generate texture description
    if results['powdery_mildew']:
        results['texture_description'] = "White powdery coating detected (possible powdery mildew)"
    elif results['rust']:
        results['texture_description'] = "Orange/brown spots detected (possible rust)"
    else:
        results['texture_description'] = "Texture appears normal"

    logger.info(f"Texture analysis: {results['texture_description']}")

    return results

# Shape and pattern analysis
def analyze_shape(images, config, logger):
    """Analyze leaf shape and patterns"""
    logger.info("Analyzing shape and patterns...")

    results = {
        'curling': False,
        'cupping': False,
        'distortion': False,
        'spotting': False,
        'shape_description': ''
    }

    # Convert to grayscale
    gray = cv2.cvtColor(images['rgb'], cv2.COLOR_RGB2GRAY)

    # Detect edges
    edges = cv2.Canny(gray, 100, 200)

    # Calculate edge density
    edge_density = np.count_nonzero(edges) / (edges.shape[0] * edges.shape[1])

    # Detect spots using thresholding
    _, thresholded = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Find contours
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Analyze contours for spotting
    spot_count = 0
    for contour in contours:
        area = cv2.contourArea(contour)
        # Spots are typically small (10-1000 pixels depending on image size)
        if 10 < area < 1000:
            spot_count += 1

    results['spotting'] = spot_count > 10

    # Simple distortion detection based on edge irregularity
    # This is a simplified approach
    results['distortion'] = edge_density > 0.15

    # Generate shape description
    if results['spotting']:
        results['shape_description'] = f"Multiple spots detected ({spot_count} spots)"
    elif results['distortion']:
        results['shape_description'] = "Irregular shape or distortion detected"
    else:
        results['shape_description'] = "Shape and patterns appear normal"

    logger.info(f"Shape analysis: {results['shape_description']}")

    return results

# Comprehensive analysis
def comprehensive_analysis(image_path, plant_id, config, logger):
    """Perform comprehensive plant health analysis"""
    logger.info(f"Starting comprehensive analysis for plant {plant_id}...")

    try:
        # Preprocess image
        images = preprocess_image(image_path, config, logger)

        # Run analyses
        color_results = analyze_color(images, config, logger)
        texture_results = analyze_texture(images, config, logger)
        shape_results = analyze_shape(images, config, logger)

        # Calculate overall health score
        issues_found = 0
        total_checks = 9  # Number of health indicators checked

        if color_results['chlorosis']:
            issues_found += 1
        if color_results['necrosis']:
            issues_found += 1
        if color_results['purpling']:
            issues_found += 1
        if texture_results['powdery_mildew']:
            issues_found += 2
        if texture_results['rust']:
            issues_found += 2
        if shape_results['spotting']:
            issues_found += 1
        if shape_results['distortion']:
            issues_found += 1
        if color_results['color_deviation'] > 0.5:
            issues_found += 1

        health_score = max(0, 100 - (issues_found * 15))

        # Determine primary issue
        primary_issue = None
        if texture_results['powdery_mildew']:
            primary_issue = "Possible powdery mildew"
        elif texture_results['rust']:
            primary_issue = "Possible rust infection"
        elif color_results['chlorosis']:
            primary_issue = "Chlorosis (yellowing) - possible nutrient deficiency"
        elif color_results['necrosis']:
            primary_issue = "Necrosis (dead tissue)"
        elif shape_results['spotting']:
            primary_issue = "Leaf spotting"

        # Compile results
        analysis_results = {
            'plant_id': plant_id,
            'image_path': image_path,
            'analysis_date': datetime.now().isoformat(),
            'analysis_mode': config['ANALYSIS_MODE'],
            'overall_health_score': health_score,
            'primary_issue': primary_issue,
            'color_analysis': color_results,
            'texture_analysis': texture_results,
            'shape_analysis': shape_results,
            'issues_detected': []
        }

        # Collect detected issues
        if color_results['chlorosis']:
            analysis_results['issues_detected'].append('Chlorosis')
        if color_results['necrosis']:
            analysis_results['issues_detected'].append('Necrosis')
        if texture_results['powdery_mildew']:
            analysis_results['issues_detected'].append('Powdery mildew')
        if texture_results['rust']:
            analysis_results['issues_detected'].append('Rust')
        if shape_results['spotting']:
            analysis_results['issues_detected'].append('Leaf spots')

        logger.info(f"Analysis complete. Health score: {health_score}/100")

        return analysis_results

    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        raise

# Save analysis to database
def save_analysis(analysis_results, config, logger):
    """Save analysis results to database"""
    db_path = config['PLANT_DB_PATH']

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Insert analysis record
        cursor.execute("""
        INSERT INTO analyses (plant_id, analysis_date, analysis_mode, overall_health_score,
                             primary_issue, issues_detected, confidence)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            analysis_results['plant_id'],
            analysis_results['analysis_date'],
            analysis_results['analysis_mode'],
            analysis_results['overall_health_score'],
            analysis_results['primary_issue'],
            ','.join(analysis_results['issues_detected']),
            0.85  # Placeholder confidence score
        ))

        analysis_id = cursor.lastrowid
        logger.info(f"Analysis saved to database with ID: {analysis_id}")

        # Insert image record
        if 'image_path' in analysis_results:
            cursor.execute("""
            INSERT INTO images (plant_id, file_path, capture_date, image_type)
            VALUES (?, ?, ?, ?)
            """, (
                analysis_results['plant_id'],
                analysis_results['image_path'],
                analysis_results['analysis_date'],
                'analysis'
            ))

            # Update analysis with image_id
            image_id = cursor.lastrowid
            cursor.execute("""
            UPDATE analyses SET image_id = ? WHERE id = ?
            """, (image_id, analysis_id))

        conn.commit()
        conn.close()

        return analysis_id

    except sqlite3.Error as e:
        logger.error(f"Database error: {str(e)}")
        raise

# Generate recommendations
def generate_recommendations(analysis_results, config, logger):
    """Generate care recommendations based on analysis"""
    logger.info("Generating recommendations...")

    recommendations = []
    preferred_approach = config.get('PREFERRED_APPROACH', 'organic')

    # Color-based recommendations
    if analysis_results['color_analysis']['chlorosis']:
        if preferred_approach in ['organic', 'balanced']:
            recommendations.append({
                'category': 'Nutrient',
                'urgency': 'medium',
                'recommendation': 'Apply organic nitrogen source such as fish emulsion or compost tea. Check soil pH if problem persists.',
                'organic': True
            })
        else:
            recommendations.append({
                'category': 'Nutrient',
                'urgency': 'medium',
                'recommendation': 'Apply balanced fertilizer with nitrogen. Consider soil pH adjustment if needed.',
                'organic': False
            })

    # Disease-based recommendations
    if analysis_results['texture_analysis']['powdery_mildew']:
        if preferred_approach in ['organic', 'balanced']:
            recommendations.append({
                'category': 'Disease',
                'urgency': 'high',
                'recommendation': 'Apply neem oil or sulfur spray. Improve air circulation around plants. Remove severely infected leaves.',
                'organic': True
            })
        else:
            recommendations.append({
                'category': 'Disease',
                'urgency': 'high',
                'recommendation': 'Apply appropriate fungicide. Remove severely infected leaves to prevent spread.',
                'organic': False
            })

    # General health recommendations
    if analysis_results['overall_health_score'] < 70:
        recommendations.append({
            'category': 'General',
            'urgency': 'medium',
            'recommendation': 'Monitor closely over next week. Check watering schedule and environmental conditions.',
            'organic': True
        })

    if analysis_results['overall_health_score'] < 50:
        recommendations.append({
            'category': 'General',
            'urgency': 'high',
            'recommendation': 'Consider consulting a horticultural expert. Multiple issues detected requiring careful attention.',
            'organic': True
        })

    logger.info(f"Generated {len(recommendations)} recommendations")

    return recommendations

def main():
    parser = argparse.ArgumentParser(description='Analyze plant health from image')
    parser.add_argument('--image', '-i', required=True, help='Path to plant image')
    parser.add_argument('--plant-id', '-p', type=int, help='Plant ID in database')
    parser.add_argument('--output', '-o', help='Output file for results (JSON)')
    parser.add_argument('--database', '-d', help='Database path (overrides .env)')
    parser.add_argument('--mode', '-m', choices=['basic', 'standard', 'comprehensive'],
                       help='Analysis mode (overrides .env)')

    args = parser.parse_args()

    # Load configuration
    config = load_config()

    # Override config with command line arguments
    if args.mode:
        config['ANALYSIS_MODE'] = args.mode
    if args.database:
        config['PLANT_DB_PATH'] = args.database

    # Setup logging
    logger = setup_logging(config)

    try:
        # Validate image
        if not os.path.exists(args.image):
            logger.error(f"Image not found: {args.image}")
            return 1

        # Perform analysis
        analysis_results = comprehensive_analysis(
            args.image,
            args.plant_id or 1,  # Default plant ID if not specified
            config,
            logger
        )

        # Generate recommendations
        recommendations = generate_recommendations(analysis_results, config, logger)
        analysis_results['recommendations'] = recommendations

        # Save to database
        if args.plant_id:
            try:
                analysis_id = save_analysis(analysis_results, config, logger)
                analysis_results['analysis_id'] = analysis_id
            except Exception as e:
                logger.warning(f"Could not save to database: {e}")

        # Output results
        print("\n" + "="*60)
        print("PLANT HEALTH ANALYSIS RESULTS")
        print("="*60)
        print(f"Image: {args.image}")
        print(f"Analysis Date: {analysis_results['analysis_date']}")
        print(f"Overall Health Score: {analysis_results['overall_health_score']}/100")
        print(f"\nPrimary Issue: {analysis_results['primary_issue'] or 'None detected'}")

        if analysis_results['issues_detected']:
            print(f"\nIssues Detected:")
            for issue in analysis_results['issues_detected']:
                print(f"  - {issue}")

        if recommendations:
            print(f"\nRecommendations:")
            for i, rec in enumerate(recommendations, 1):
                print(f"\n{i}. [{rec['category'].upper()}] {rec['urgency'].upper()}")
                print(f"   {rec['recommendation']}")
                if rec['organic']:
                    print(f"   (Organic method)")

        print("\n" + "="*60)

        # Save to file if requested
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(analysis_results, f, indent=2)
            logger.info(f"Results saved to: {args.output}")

        return 0

    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
