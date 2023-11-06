import os

from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim


class Geocoder:
    def __init__(self):
        # Initialize the geolocator with a user agent
        self.geolocator = Nominatim(user_agent=os.environ.get('SECRET_KEY', 'ABSTRACT_CHALLENGE_j'))

    @staticmethod
    def handle_exception(e):
        # Handle common exceptions
        if isinstance(e, ValueError):
            return {"error": "Invalid Coordinates"}
        if isinstance(e, GeocoderTimedOut):
            return {"error": "Geocoding timed out"}
        return {"error": str(e)}

    def geocode_from_location_name(self, location_name):
        try:
            # Geocode a location name to get latitude and longitude
            location = self.geolocator.geocode(location_name)
            if location is not None:
                return {"latitude": location.latitude, "longitude": location.longitude}
            else:
                return {"error": "Location not found"}
        except Exception as e:
            return Geocoder.handle_exception(e)

    def reverse_geocode(self, latitude, longitude):
        try:
            # Reverse geocode latitude and longitude to get location details
            location = self.geolocator.reverse((latitude, longitude))
            if location is not None:
                country = location.raw.get("address", {}).get("country")
                city = location.raw.get("address", {}).get("state", location.raw.get("address", {}).get("city"))

                result = {
                    'country': country if country else 'Unknown',
                    'name': city if city else 'Unknown',
                    'latitude': location.latitude,
                    'longitude': location.longitude
                }
                return result
            else:
                return {"error": "Location not found"}
        except Exception as e:
            return Geocoder.handle_exception(e)
