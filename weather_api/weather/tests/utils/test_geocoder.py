import unittest
from unittest.mock import Mock, patch

from weather.utils.geocoder import Geocoder


class GeocoderTest(unittest.TestCase):
    def setUp(self):
        self.geocoder = Geocoder()

    def test_geocode_from_location_name_success(self):
        location_name = "New York"
        with patch.object(self.geocoder.geolocator, "geocode") as mock_geocode:
            mock_geocode.return_value = Mock(latitude=40.7128, longitude=-74.0060)
            result = self.geocoder.geocode_from_location_name(location_name)
            self.assertEqual(result, {"latitude": 40.7128, "longitude": -74.0060})

    def test_geocode_from_location_name_location_not_found(self):
        location_name = "Invalid Location"
        with patch.object(self.geocoder.geolocator, "geocode") as mock_geocode:
            mock_geocode.return_value = None
            result = self.geocoder.geocode_from_location_name(location_name)
            self.assertEqual(result, {"error": "Location not found"})

    def test_geocode_from_location_name_exception(self):
        location_name = "Some Location"
        with patch.object(self.geocoder.geolocator, "geocode") as mock_geocode:
            mock_geocode.side_effect = Exception("Geocoding Error")
            result = self.geocoder.geocode_from_location_name(location_name)
            self.assertEqual(result, {"error": "Geocoding Error"})

    def test_reverse_geocode_success(self):
        latitude, longitude = 40.7128, -74.0060
        with patch.object(self.geocoder.geolocator, "reverse") as mock_reverse:
            mock_reverse.return_value = Mock(
                raw={"address": {"country": "USA", "city": "New York"}},
                latitude=latitude, longitude=longitude
            )

            result = self.geocoder.reverse_geocode(latitude, longitude)
            self.assertEqual(result, {"country": "USA", "name": "New York", "latitude": 40.7128, "longitude": -74.0060})

    def test_reverse_geocode_location_not_found(self):
        latitude, longitude = 40.7128, -74.0060
        with patch.object(self.geocoder.geolocator, "reverse") as mock_reverse:
            mock_reverse.return_value = None
            result = self.geocoder.reverse_geocode(latitude, longitude)
            self.assertEqual(result, {"error": "Location not found"})

    def test_reverse_geocode_exception(self):
        latitude, longitude = 40.7128, -74.0060
        with patch.object(self.geocoder.geolocator, "reverse") as mock_reverse:
            mock_reverse.side_effect = Exception("Reverse Geocoding Error")
            result = self.geocoder.reverse_geocode(latitude, longitude)
            self.assertEqual(result, {"error": "Reverse Geocoding Error"})


if __name__ == '__main__':
    unittest.main()
