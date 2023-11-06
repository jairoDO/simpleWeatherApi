import functools
import random
from datetime import timedelta

import pytz
import requests
from django.utils import timezone as dj_timezone

# List of common city names
global common_city_names
common_city_names = [
    "New York",
    "Paris",
    "London",
    "Tokyo",
    "Mexico City",
    "Sydney",
    "Rio de Janeiro",
    "Dubai",
    "Rome",
    "Beijing",
    "Los Angeles",
    "Buenos Aires",
    "Berlin",
    "Istanbul",
    "Moscow",
    "Toronto",
    "Bangkok",
    "Cairo",
    "Amsterdam",
    "Nairobi"
]


@functools.lru_cache(maxsize=None)
def get_country_names():
    try:
        # Get a list of country names from a REST API
        response = requests.get("https://restcountries.com/v3.1/all")
        data = response.json()
        country_names = [country["name"]["common"] for country in data]
        return country_names
    except Exception as e:
        # Handle any exceptions
        print(f"Error: {e}")
        return []


@functools.lru_cache(maxsize=None)
def get_city_names():
    try:
        # Get a list of city names from the Geonames API
        response = requests.get(
            "http://api.geonames.org/searchJSON",
            params={"q": "city", "maxRows": 10, "username": "demo"}
        )
        data = response.json()
        # Extract city names from the response
        city_names = [entry["name"] for entry in data["geonames"]]
        return city_names
    except Exception as e:
        # Handle any exceptions, including when the Geonames demo limit is exceeded
        print(f"Warning Geonames demo has exceeded: {e}")
        return common_city_names


def generate_random_location_data(geocoder_instance):
    # List of random countries
    generated = False
    while not generated:
        # Latitude range: approximately -90 to 90 (covers the entire globe)
        latitude = round(random.uniform(-90, 90), 6)
        # Longitude range: approximately -180 to 180 (covers the entire globe)
        longitude = round(random.uniform(-180, 180), 6)
        location_data = geocoder_instance.reverse_geocode(latitude, longitude)
        if 'error' not in location_data:
            return location_data


def generate_random_weather_data():
    # Generate random weather data
    temperature = round(random.uniform(-20, 40), 2)
    condition = random.choice(
        ["Thunderstorm", "Drizzle", "Rain", "Snow", "Mist", "Smoke", "Haze", "Dust", "Fog", "Sand", "Dust", "Ash",
         "Squall", "Tornado", "Clear", "Clouds"]
    )
    pressure = random.randint(950, 1050)
    humidity = random.randint(0, 100)
    sea_level = random.randint(950, 1050)
    ground_level = random.randint(950, 1050)
    visibility = round(random.uniform(0, 10), 2)  
    wind_speed = round(random.uniform(0, 30), 2)
    wind_direction = random.randint(0, 360)
    clouds = random.randint(0, 100)
    rain_1h = round(random.uniform(0, 50), 2)  
    timezone = random.choice(list(pytz.all_timezones))
    data_timestamp = dj_timezone.now()
    sunrise = data_timestamp - timedelta(hours=random.randint(4, 6))
    sunset = data_timestamp + timedelta(hours=random.randint(6, 10))
    
    return {
        "temperature": temperature,
        "condition": condition,
        "pressure": pressure,
        "humidity": humidity,
        "sea_level": sea_level,
        "ground_level": ground_level,
        "visibility": visibility,
        "wind_speed": wind_speed,
        "wind_direction": wind_direction,
        "clouds": clouds,
        "rain_1h": rain_1h,
        "data_timestamp": data_timestamp,
        "timezone": timezone,
        "sunrise": sunrise,
        "sunset": sunset,
    }
