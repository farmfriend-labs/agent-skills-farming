#!/usr/bin/env python3
"""
weather_feed.py - Weather Data Simulator
Generates realistic weather data and forecasts.
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
logger = logging.getLogger('WeatherFeedSimulator')


@dataclass
class WeatherReading:
    """Represents weather reading."""
    location: str
    temperature: float
    temperature_unit: str
    humidity: float
    humidity_unit: str
    wind_speed: float
    wind_speed_unit: str
    wind_direction: str
    pressure: float
    pressure_unit: str
    precipitation: float
    precipitation_unit: str
    visibility: float
    visibility_unit: str
    cloud_cover: float
    cloud_cover_unit: str
    feels_like: float
    feels_like_unit: str
    gdd: float
    et: float
    timestamp: str


class WeatherFeedSimulator:
    """Simulates weather data and forecasts."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.output_file = None
        self.location = config.get('location', 'Unknown')
        self.timezone = config.get('timezone', 'America/Chicago')
        self.update_interval = config.get('update_interval_minutes', 15) * 60
        self.include_forecast = config.get('include_forecast', True)
        self.include_alerts = config.get('include_alerts', True)
        self.gdd_base_temp = config.get('gdd_base_temp', 50)
        self.gdd_max_temp = config.get('gdd_max_temp', 86)

        # Current conditions
        self.current_temp = random.uniform(45, 85)
        self.current_humidity = random.uniform(40, 80)
        self.current_wind = random.uniform(2, 15)
        self.current_pressure = random.uniform(29.5, 30.5)

        # GDD accumulator
        self.gdd_accumulator = 0.0

        # Setup output
        self.setup_output()

    def setup_output(self):
        """Setup output file."""
        output_dir = Path(__file__).parent.parent / "outputs"
        output_dir.mkdir(exist_ok=True)

        self.output_file = output_dir / "weather.json"
        logger.info(f"Output file: {self.output_file}")

    def fluctuate_current_conditions(self):
        """Fluctuate current weather conditions slightly."""
        # Temperature fluctuates slowly
        temp_change = random.uniform(-2, 2)
        self.current_temp = max(20, min(110, self.current_temp + temp_change))

        # Humidity fluctuates
        humidity_change = random.uniform(-5, 5)
        self.current_humidity = max(10, min(100, self.current_humidity + humidity_change))

        # Wind fluctuates
        wind_change = random.uniform(-3, 3)
        self.current_wind = max(0, min(50, self.current_wind + wind_change))

        # Pressure fluctuates slowly
        pressure_change = random.uniform(-0.1, 0.1)
        self.current_pressure = max(29.0, min(31.0, self.current_pressure + pressure_change))

    def calculate_gdd(self) -> float:
        """Calculate growing degree days."""
        # Daily GDD calculation
        if self.current_temp < self.gdd_base_temp:
            daily_gdd = 0.0
        elif self.current_temp > self.gdd_max_temp:
            daily_gdd = (self.gdd_max_temp - self.gdd_base_temp) / 2.0
        else:
            daily_gdd = (self.current_temp - self.gdd_base_temp) / 2.0

        # Accumulate
        self.gdd_accumulator += daily_gdd
        return self.gdd_accumulator

    def calculate_et(self) -> float:
        """Calculate evapotranspiration (simplified)."""
        # Simplified Penman-Monteith
        # ET = f(T) * g(humidity)
        temperature_factor = 0.0 + (self.current_temp / 100.0) * 0.8
        humidity_factor = 1.0 - (self.current_humidity / 100.0) * 0.3
        wind_factor = 1.0 + (self.current_wind / 20.0) * 0.2

        et = temperature_factor * humidity_factor * wind_factor * 0.1
        return round(et, 3)

    def get_wind_direction(self, wind_speed: float) -> str:
        """Get wind direction based on speed and randomness."""
        directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        return random.choice(directions)

    def generate_current_conditions(self) -> WeatherReading:
        """Generate current weather conditions."""
        self.fluctuate_current_conditions()

        # Calculate derived metrics
        gdd = self.calculate_gdd()
        et = self.calculate_et()
        wind_direction = self.get_wind_direction(self.current_wind)

        # Calculate feels-like temperature
        heat_index = self.current_temp
        if self.current_temp >= 80 and self.current_humidity >= 40:
            # Simplified heat index
            heat_index = self.current_temp + (self.current_humidity / 100.0) * 10.0

        reading = WeatherReading(
            location=self.location,
            temperature=round(self.current_temp, 1),
            temperature_unit='F',
            humidity=round(self.current_humidity, 0),
            humidity_unit='%',
            wind_speed=round(self.current_wind, 1),
            wind_speed_unit='mph',
            wind_direction=wind_direction,
            pressure=round(self.current_pressure, 2),
            pressure_unit='inHg',
            precipitation=random.uniform(0, 0.1),
            precipitation_unit='in',
            visibility=random.uniform(5, 15),
            visibility_unit='mi',
            cloud_cover=random.uniform(0, 100),
            cloud_cover_unit='%',
            feels_like=round(heat_index, 1),
            feels_like_unit='F',
            gdd=round(gdd, 1),
            et=et,
            timestamp=datetime.utcnow().isoformat()
        )

        return reading

    def generate_forecast(self, hours_ahead: int = 48) -> List[Dict]:
        """Generate weather forecast."""
        forecast = []
        temp = self.current_temp
        humidity = self.current_humidity
        wind = self.current_wind

        for hour in range(0, hours_ahead + 1, 3):
            # Fluctuate conditions
            temp_change = random.uniform(-1.5, 1.5)
            temp = max(20, min(110, temp + temp_change))

            humidity_change = random.uniform(-8, 8)
            humidity = max(10, min(100, humidity + humidity_change))

            wind_change = random.uniform(-5, 5)
            wind = max(0, min(40, wind + wind_change))

            # Determine conditions
            conditions = 'sunny'
            if humidity > 80:
                conditions = 'cloudy'
            elif humidity > 90:
                conditions = 'rainy'
            elif wind > 20:
                conditions = 'windy'

            forecast_item = {
                'hour': hour,
                'datetime': (datetime.utcnow() + timedelta(hours=hour)).isoformat(),
                'temperature': round(temp, 1),
                'temperature_unit': 'F',
                'humidity': round(humidity, 0),
                'humidity_unit': '%',
                'wind_speed': round(wind, 1),
                'wind_speed_unit': 'mph',
                'wind_direction': random.choice(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']),
                'conditions': conditions,
                'precipitation_chance': random.randint(0, 30),
                'precipitation_amount': round(random.uniform(0, 0.2), 2)
            }

            forecast.append(forecast_item)

        return forecast

    def generate_alerts(self) -> List[Dict]:
        """Generate weather alerts based on conditions."""
        alerts = []
        alert_thresholds = self.config.get('alert_thresholds', {})

        # Freeze alert
        if 'freeze' in alert_thresholds:
            freeze_threshold = alert_thresholds['freeze']['temperature']
            hours_ahead = alert_thresholds['freeze']['hours_ahead']

            if self.current_temp <= freeze_threshold:
                alerts.append({
                    'type': 'freeze',
                    'severity': 'warning',
                    'message': f'Freeze warning: Temperature at {round(self.current_temp, 1)}F',
                    'hours_ahead': hours_ahead,
                    'action_required': 'Protect crops and equipment'
                })

        # Wind alert
        if 'wind' in alert_thresholds:
            wind_threshold = alert_thresholds['wind']['speed_mph']
            hours_ahead = alert_thresholds['wind']['hours_ahead']

            if self.current_wind >= wind_threshold:
                alerts.append({
                    'type': 'high_wind',
                    'severity': 'warning',
                    'message': f'High wind warning: {round(self.current_wind, 1)} mph',
                    'hours_ahead': hours_ahead,
                    'action_required': 'Delay spraying and aerial operations'
                })

        # Heat alert
        if 'heat' in alert_thresholds:
            heat_threshold = alert_thresholds['heat']['temperature']
            hours_ahead = alert_thresholds['heat']['hours_ahead']

            if self.current_temp >= heat_threshold:
                alerts.append({
                    'type': 'heat_advisory',
                    'severity': 'advisory',
                    'message': f'Heat advisory: Temperature at {round(self.current_temp, 1)}F',
                    'hours_ahead': hours_ahead,
                    'action_required': 'Ensure livestock shade and water'
                })

        return alerts

    def generate_all_weather_data(self) -> Dict:
        """Generate complete weather data."""
        weather_data = {
            'location': self.location,
            'timezone': self.timezone,
            'current_conditions': asdict(self.generate_current_conditions()),
            'timestamp': datetime.utcnow().isoformat()
        }

        # Add forecast
        if self.include_forecast:
            weather_data['forecast'] = self.generate_forecast(hours_ahead=48)

        # Add alerts
        if self.include_alerts:
            weather_data['alerts'] = self.generate_alerts()

        return weather_data

    def write_output(self, data: Dict):
        """Write weather data to output file."""
        with open(self.output_file, 'w') as f:
            json.dump(data, f, indent=2)

    def run(self, duration_seconds: int = None):
        """Run weather feed simulator."""
        logger.info("Starting weather feed simulator...")
        logger.info(f"Location: {self.location}")
        logger.info(f"Timezone: {self.timezone}")
        logger.info(f"Update interval: {self.update_interval // 60} minutes")

        start_time = time.time()
        update_count = 0

        try:
            while duration_seconds is None or time.time() - start_time < duration_seconds:
                # Generate weather data
                data = self.generate_all_weather_data()

                # Write output
                self.write_output(data)
                update_count += 1

                current_temp = data['current_conditions']['temperature']
                logger.debug(f"Update {update_count}: Current temp {current_temp}F, "
                           f"{len(data.get('alerts', []))} alerts")

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
            "location": self.location,
            "timezone": self.timezone,
            "update_interval_minutes": self.update_interval // 60,
            "include_forecast": self.include_forecast,
            "include_alerts": self.include_alerts,
            "gdd_base_temp": self.gdd_base_temp,
            "gdd_max_temp": self.gdd_max_temp,
        }


def main():
    parser = argparse.ArgumentParser(description="Weather Feed Simulator")

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
    simulator = WeatherFeedSimulator(config)

    # Print stats and exit
    if args.stats:
        stats = simulator.get_stats()
        print(json.dumps(stats, indent=2))
        return

    # Run simulator
    simulator.run(duration_seconds=args.duration)


if __name__ == "__main__":
    main()
