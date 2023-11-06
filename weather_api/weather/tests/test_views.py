from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from weather.utils.geocoder import Geocoder


class WeatherViewsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.geocoder = Geocoder()

    def test_get_current_weather_with_positive_coordinates(self):
        latitude, longitude = 12.34, 56.78
        url = reverse('get-current-weather', args=[latitude, longitude])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_current_weather_with_negative_coordinates(self):
        latitude, longitude = -12.0464, -12.0464
        url = reverse('get-current-weather', args=[latitude, longitude])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_current_weather_invalid_location(self):
        # Test with an invalid location that should return random weather data
        response = self.client.get('/weather/api/get_current_weather/InvalidLocation/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_current_weather_negative_values(self):
        # Test with negative latitude and longitude values
        response = self.client.get('/weather/api/get_current_weather/-12.0464/-12.0464/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_current_weather_invalid_longitude(self):
        response = self.client.get('/weather/api/get_current_weather/-40.7128/-200.0060/')
        expected_data = {
            "error": {
                "location": {
                    "longitude": [
                        "Longitude must be in the range of -180 to 180 degrees."
                    ]
                }
            }
        }
        self.assertDictEqual(expected_data, response.json(), "The longitude validator is not working propertly")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_current_weather_invalid_latitude(self):
        response = self.client.get('/weather/api/get_current_weather/-200.0060/-40.7128/')
        expected_data = {
            "error": {
                "location": {
                    "latitude": [
                        "Latitude must be in the range of -90 to 90 degrees."
                    ]
                }
            }
        }
        self.assertDictEqual(expected_data, response.json(), "The latitude validator is not working propertly")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_current_weather_invalid_data(self):
        # Test with invalid data that should return an error
        response = self.client.get('/weather/api/get_current_weather/40.7128/invalid_longitude/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_coordinates_by_location_name(self):
        location_name = "New York"
        url = reverse('get-coordinates', args=[location_name])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_coordinates_by_invalidate_location(self):
        # Test with an invalid location that should return an error
        response = self.client.get('/weather/api/get_coordinates/InvalidLocation/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_geocode_from_location_name_invalid_location(self):
        location_name = "Nonexistent Place"
        result = self.geocoder.geocode_from_location_name(location_name)
        self.assertEqual(result.get("error"), "Location not found")

    def test_reverse_geocode_valid_coordinates(self):
        latitude, longitude = 40.7128, -74.0060  # New York coordinates
        result = self.geocoder.reverse_geocode(latitude, longitude)
        self.assertIn("country", result)
        self.assertIn("name", result)

    def test_reverse_geocode_invalid_coordinates(self):
        latitude, longitude = 999.99, 888.88  # Invalid coordinates
        result = self.geocoder.reverse_geocode(latitude, longitude)
        self.assertEqual(result.get("error"), "Invalid Coordinates")
