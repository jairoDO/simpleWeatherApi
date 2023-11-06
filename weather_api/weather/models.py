from django.db import models
from .validators import validate_latitude, validate_longitude

from .utils.random_data import generate_random_weather_data, generate_random_location_data


class Location(models.Model):
    country = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    latitude = models.FloatField(validators=[validate_latitude])
    longitude = models.FloatField(validators=[validate_longitude])

    def __str__(self):
        return f"{self.name}, {self.country}"


class Weather(models.Model):
    temperature = models.FloatField()  # Temperature in Celsius
    condition = models.CharField(max_length=20)  # Weather condition (e.g., Clear, Rain, Snow)
    pressure = models.FloatField()  # Atmospheric pressure in hPa
    humidity = models.FloatField()  # Humidity in percentage
    sea_level = models.FloatField()  # Atmospheric pressure at sea level in hPa
    ground_level = models.FloatField()  # Atmospheric pressure at ground level in hPa
    visibility = models.FloatField()  # Visibility in meters
    wind_speed = models.FloatField()  # Wind speed in meter/second
    wind_direction = models.FloatField()  # Wind direction in degrees
    clouds = models.FloatField()  # Cloudiness in percentage
    rain_1h = models.FloatField()  # Rain volume in the last 1 hour in mm
    data_timestamp = models.DateTimeField(auto_now_add=True)  # Time of data calculation in UTC
    timezone = models.CharField(max_length=63)  # Shift in seconds from UTC
    sunrise = models.DateTimeField()  # Sunrise time in UTC
    sunset = models.DateTimeField()  # Sunset time in UTC
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return f"Weather in {self.location} - {self.data_timestamp}"
    
    @classmethod
    def generate_random_weather_with_real_location(cls, geocoder_instance, location_data=None, choose_instance=False):
        
        weather_random = generate_random_weather_data()
        if not location_data:
            location_data = generate_random_location_data(geocoder_instance=geocoder_instance)

        # Try to find a Location instance with the same coordinates
        location_instance, _ = Location.objects.get_or_create(**location_data)

        if choose_instance:
            weather_random['location'] = location_instance
        else:
            weather_random["location"] = location_data

        return weather_random
    
