#!/usr/bin/env python3
"""
Main script for actionable-weather-alerts
"""
import sys
import argparse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Actionable Weather Alerts")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    logger.info("Actionable Weather Alerts running...")
    # Add main functionality here
    logger.info("Complete")

if __name__ == "__main__":
    main()
