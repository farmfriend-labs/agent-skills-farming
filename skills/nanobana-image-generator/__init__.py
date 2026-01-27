#!/usr/bin/env python3
"""
Nano Banana wrapper - Importable module for direct use
"""
import sys
sys.path.insert(0, '/home/scrimwiggins/clawd/skills/nanobana-image-generator')

from simple_generate import generate_image, edit_image

__all__ = ['generate_image', 'edit_image']
