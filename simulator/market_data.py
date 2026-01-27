#!/usr/bin/env python3
"""
market_data.py - Market Data Simulator
Generates realistic agricultural market data.
"""

import sys
import json
import time
import argparse
import logging
import random
from typing import Dict, List, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('MarketDataSimulator')


@dataclass
class CommodityPrice:
    """Represents commodity pricing."""
    commodity: str
    price: float
    unit: str
    basis: float
    cash_bid: float
    change: float
    change_percent: float
    timestamp: str


class MarketDataSimulator:
    """Simulates agricultural market data."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.output_file = None
        self.commodities = config.get('commodities', [])
        self.update_interval = config.get('update_interval_minutes', 15) * 60
        self.include_futures = config.get('include_futures', True)
        self.include_local_bids = config.get('include_local_bids', True)
        self.include_premiums = config.get('include_premiums', True)
        self.location = config.get('location', 'Unknown')

        # Base prices (per bushel, roughly)
        self.base_prices = {
            'corn': 4.25,
            'soybeans': 11.80,
            'wheat': 5.90,
            'cotton': 0.80,
            'sorghum': 3.75
        }

        # Current prices (will fluctuate)
        self.current_prices = self.base_prices.copy()

        # Setup output
        self.setup_output()

    def setup_output(self):
        """Setup output file."""
        output_dir = Path(__file__).parent.parent / "outputs"
        output_dir.mkdir(exist_ok=True)

        self.output_file = output_dir / "market-data.json"
        logger.info(f"Output file: {self.output_file}")

    def fluctuate_price(self, commodity: str, max_change_percent: float = 0.02) -> float:
        """Fluctuate price slightly."""
        current = self.current_prices[commodity]
        max_change = current * max_change_percent
        change = random.uniform(-max_change, max_change)
        new_price = current + change
        self.current_prices[commodity] = new_price
        return new_price

    def calculate_basis(self, commodity: str) -> float:
        """Calculate basis (difference from futures)."""
        # Typical basis values (can be positive or negative)
        basis_ranges = {
            'corn': (-0.50, 0.30),
            'soybeans': (-0.75, 0.50),
            'wheat': (-0.60, 0.40),
            'cotton': (-0.15, 0.10),
            'sorghum': (-0.40, 0.25)
        }

        if commodity in basis_ranges:
            min_basis, max_basis = basis_ranges[commodity]
            return random.uniform(min_basis, max_basis)

        return 0.0

    def get_local_bid(self, commodity: str) -> float:
        """Get local elevator bid."""
        elevators = self.config.get('elevators', [])

        if not elevators:
            return self.current_prices[commodity]

        # Get bids from random elevator
        elevator = random.choice(elevators)
        elevator_bids = elevator.get('bids', {})

        if commodity in elevator_bids:
            base_bid = elevator_bids[commodity]
            # Add small fluctuation
            fluctuation = random.uniform(-0.03, 0.03)
            return base_bid + fluctuation

        return self.current_prices[commodity]

    def generate_commodity_pricing(self, commodity: str) -> Dict:
        """Generate pricing for a commodity."""
        # Fluctuate price
        price = self.fluctuate_price(commodity)

        # Calculate change
        base_price = self.base_prices[commodity]
        change = price - base_price
        change_percent = (change / base_price) * 100 if base_price > 0 else 0

        # Calculate basis
        basis = self.calculate_basis(commodity)

        # Get local bid
        cash_bid = self.get_local_bid(commodity)

        # Futures price (price - basis)
        futures_price = price - basis

        pricing = {
            'commodity': commodity,
            'futures_price': round(futures_price, 2),
            'basis': round(basis, 2),
            'cash_bid': round(cash_bid, 2),
            'change': round(change, 2),
            'change_percent': round(change_percent, 2),
            'unit': 'USD/bu' if commodity in ['corn', 'soybeans', 'wheat', 'sorghum'] else 'USD/lb'
        }

        # Add futures exchange
        if self.include_futures:
            exchanges = {
                'corn': 'CBOT',
                'soybeans': 'CBOT',
                'wheat': 'KCBT',
                'cotton': 'ICE'
            }
            pricing['futures_exchange'] = exchanges.get(commodity, 'Unknown')

        return pricing

    def generate_premium_opportunities(self) -> List[Dict]:
        """Generate premium market opportunities."""
        premiums = []
        premium_opportunities = self.config.get('premium_opportunities', {})

        for market_type, premium_config in premium_opportunities.items():
            premium_percent = premium_config.get('premium_percent', 0)
            if premium_percent == 0:
                continue

            for commodity in self.commodities:
                base = self.current_prices[commodity]
                premium = base * (premium_percent / 100)
                premium_price = base + premium

                opportunities = {
                    'market_type': market_type,
                    'commodity': commodity,
                    'base_price': round(base, 2),
                    'premium': round(premium, 2),
                    'premium_price': round(premium_price, 2),
                    'premium_percent': premium_percent
                }
                premiums.append(opportunities)

        return premiums

    def generate_all_market_data(self) -> Dict:
        """Generate complete market data."""
        market_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'location': self.location,
            'commodities': [],
            'premiums': []
        }

        # Generate pricing for each commodity
        for commodity in self.commodities:
            if commodity in self.current_prices:
                pricing = self.generate_commodity_pricing(commodity)
                market_data['commodities'].append(pricing)

        # Generate premium opportunities
        if self.include_premiums:
            market_data['premiums'] = self.generate_premium_opportunities()

        return market_data

    def write_output(self, data: Dict):
        """Write market data to output file."""
        with open(self.output_file, 'w') as f:
            json.dump(data, f, indent=2)

    def run(self, duration_seconds: int = None):
        """Run market data simulator."""
        logger.info("Starting market data simulator...")
        logger.info(f"Commodities: {', '.join(self.commodities)}")
        logger.info(f"Location: {self.location}")
        logger.info(f"Update interval: {self.update_interval // 60} minutes")

        start_time = time.time()
        update_count = 0

        try:
            while duration_seconds is None or time.time() - start_time < duration_seconds:
                # Generate market data
                data = self.generate_all_market_data()

                # Write output
                self.write_output(data)
                update_count += 1

                logger.debug(f"Update {update_count}: {len(data['commodities'])} commodities, "
                           f"{len(data['premiums'])} premiums")

                # Sleep for update interval
                time.sleep(self.update_interval)

        except KeyboardInterrupt:
            logger.info("Interrupted by user")
        finally:
            logger.info(f"Sent {update_count} updates")
            logger.info(f"Output written to: {self.output_file}")

    def get_stats(self) -> Dict:
        """Get simulator statistics."""
        return {
            "commodities": self.commodities,
            "location": self.location,
            "update_interval_minutes": self.update_interval // 60,
            "include_futures": self.include_futures,
            "include_local_bids": self.include_local_bids,
            "include_premiums": self.include_premiums,
        }


def main():
    parser = argparse.ArgumentParser(description="Market Data Simulator")

    parser.add_argument("--config", "-c", required=True,
                        help="Configuration file (JSON)")
    parser.add_argument("--duration", "-d", type=int,
                        help="Duration in seconds (default: run forever)")
    parser.add_argument("--stats", "-s", action="store_true",
                        help="Print statistics and exit")

    args = parser.parse_args()

    # Load configuration
    try:
        with open(args.config, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        logger.error(f"Configuration file not found: {args.config}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in configuration: {e}")
        sys.exit(1)

    # Create simulator
    simulator = MarketDataSimulator(config)

    # Print stats and exit
    if args.stats:
        stats = simulator.get_stats()
        print(json.dumps(stats, indent=2))
        return

    # Run simulator
    simulator.run(duration_seconds=args.duration)


if __name__ == "__main__":
    main()
