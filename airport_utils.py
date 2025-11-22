"""
Airport utilities for location-based search and flight duration calculations
"""

import json
import math
from typing import List, Dict, Optional, Tuple


class AirportDatabase:
    """Manages airport data and provides search/calculation utilities"""

    def __init__(self, data_file: str = "airports_data.json"):
        self.data_file = data_file
        self.airports: List[Dict] = []
        self.load_airports()

    def load_airports(self):
        """Load airport data from JSON file"""
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                self.airports = data.get('airports', [])
            print(f"Loaded {len(self.airports)} airports from {self.data_file}")
        except FileNotFoundError:
            print(f"Warning: Airport data file {self.data_file} not found")
            self.airports = []

    def search_airports(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search airports by location (city, state, airport name, or code)
        Returns a list of matching airports
        """
        if not query or len(query) < 2:
            return []

        query_lower = query.lower().strip()
        matches = []

        for airport in self.airports:
            # Calculate relevance score
            score = 0

            # Exact code match (highest priority)
            if airport['code'].lower() == query_lower:
                score = 1000
            # Code starts with query
            elif airport['code'].lower().startswith(query_lower):
                score = 500
            # City exact match
            elif airport['city'].lower() == query_lower:
                score = 400
            # City starts with query
            elif airport['city'].lower().startswith(query_lower):
                score = 300
            # State match
            elif airport['state'].lower() == query_lower:
                score = 200
            # Name contains query
            elif query_lower in airport['name'].lower():
                score = 100
            # City contains query
            elif query_lower in airport['city'].lower():
                score = 50

            if score > 0:
                match = airport.copy()
                match['relevance'] = score
                matches.append(match)

        # Sort by relevance (highest first)
        matches.sort(key=lambda x: x['relevance'], reverse=True)

        return matches[:limit]

    def get_airport_by_code(self, code: str) -> Optional[Dict]:
        """Get airport details by IATA code"""
        code_upper = code.upper().strip()
        for airport in self.airports:
            if airport['code'] == code_upper:
                return airport
        return None

    @staticmethod
    def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate the great circle distance between two points on Earth
        Returns distance in miles
        """
        # Convert decimal degrees to radians
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)

        # Haversine formula
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad

        a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))

        # Radius of Earth in miles
        r = 3959

        return c * r

    def calculate_distance(self, departure_code: str, destination_code: str) -> Optional[float]:
        """
        Calculate distance between two airports in miles
        Returns None if either airport is not found
        """
        dep_airport = self.get_airport_by_code(departure_code)
        dest_airport = self.get_airport_by_code(destination_code)

        if not dep_airport or not dest_airport:
            return None

        return self.haversine_distance(
            dep_airport['lat'], dep_airport['lon'],
            dest_airport['lat'], dest_airport['lon']
        )

    def estimate_flight_duration(self, departure_code: str, destination_code: str,
                                 average_speed_mph: int = 450) -> Optional[Tuple[int, int]]:
        """
        Estimate flight duration between two airports
        Returns (hours, minutes) tuple or None if airports not found

        Args:
            departure_code: IATA code of departure airport
            destination_code: IATA code of destination airport
            average_speed_mph: Average cruising speed (default 450 mph for typical private jets)
        """
        distance = self.calculate_distance(departure_code, destination_code)

        if distance is None:
            return None

        # Add time for taxi, takeoff, climb, descent, landing (approximately 30 minutes)
        ground_time_hours = 0.5

        # Calculate flight time
        flight_time_hours = distance / average_speed_mph
        total_hours = flight_time_hours + ground_time_hours

        hours = int(total_hours)
        minutes = int((total_hours - hours) * 60)

        return (hours, minutes)

    def get_airports_near_location(self, city: str, state: str = None, limit: int = 5) -> List[Dict]:
        """
        Find airports near a given city/location
        Returns list of nearby airports
        """
        results = []

        for airport in self.airports:
            if city.lower() in airport['city'].lower():
                if state is None or state.lower() in airport['state'].lower():
                    results.append(airport)

        return results[:limit]


# Global instance
airport_db = AirportDatabase()


if __name__ == "__main__":
    # Test the airport database
    print("Testing Airport Database\n" + "="*60)

    # Test search
    print("\n1. Search for 'Los Angeles':")
    results = airport_db.search_airports("Los Angeles")
    for r in results[:3]:
        print(f"  {r['code']} - {r['name']} ({r['city']}, {r['state']})")

    print("\n2. Search for 'New York':")
    results = airport_db.search_airports("New York")
    for r in results:
        print(f"  {r['code']} - {r['name']} ({r['city']}, {r['state']})")

    print("\n3. Search by code 'LAX':")
    results = airport_db.search_airports("LAX")
    for r in results:
        print(f"  {r['code']} - {r['name']} ({r['city']}, {r['state']})")

    # Test distance calculation
    print("\n4. Distance LAX to JFK:")
    distance = airport_db.calculate_distance("LAX", "JFK")
    if distance:
        print(f"  {distance:.0f} miles")

    # Test flight duration estimation
    print("\n5. Flight duration LAX to JFK:")
    duration = airport_db.estimate_flight_duration("LAX", "JFK")
    if duration:
        print(f"  {duration[0]} hours {duration[1]} minutes")

    print("\n6. Flight duration SFO to MIA:")
    duration = airport_db.estimate_flight_duration("SFO", "MIA")
    if duration:
        print(f"  {duration[0]} hours {duration[1]} minutes")
