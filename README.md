
# Weather API Implementation

This repository contains the implementation of a simple Weather API using Python, Django, and Django Rest Framework.
The API provides two main endpoints: one for accessing current weather data for a given location using latitude and 
longitude and another for transforming a location name or city name into geographical coordinates. Additionally, 
the project is designed to be Dockerized for easy deployment.

## Index

- [Tech Stack](#tech-stack)
- [Endpoints](#endpoints)
  - [1. Current Weather Data (GET and POST)](#1-current-weather-data-get-and-post)
  - [2. Coordinates by Location Name](#2-coordinates-by-location-name)
  - [3. Other Features](#3-other-features)
- [Directory Structure](#directory-structure)
- [Dockerization (Bonus)](#dockerization-bonus)
- [Usage](#usage)
- [Docker Compose Services](#docker-compose-services)
- [Testing](#testing)
- [To-Do List](#to-do-list)

## Tech Stack

- Python
- Django
- Django Rest Framework
- [geopy](https://pypi.org/project/geopy/) (for geocoding)
- Docker (optional, for containerization)

## Endpoints

### 1. Current Weather Data (GET and POST)

- **Endpoint:** `/weather/api/get_current_weather/<latitude>/<longitude>/`
- **Method:** GET and POST
- **Description:** Access current weather data for any location on Earth based on the provided latitude and longitude.
- **Response Format:** JSON
- **Functionality:** 
    - The API uses geocoding to find the nearest location based on the latitude and longitude.
    - It retrieves the most recent weather data for that location or generates random weather without storage if using get
    - For post request the result generated it saved with random data except the location. I implement this way because 
    - I consider saved in get is not good practice that breaks the principles of APIs methods. 
- **Status Codes:**
    - 200: Success, returns weather data
    - 400: Bad Request, e.g., for invalid latitude and longitude
- **Example Request (GET):** `/weather/api/get_current_weather/61.999/66.3581/`
- **Example Request (POST):** 
  ```json
  {
    "latitude": 61.999,
    "longitude": 66.3581
  }

### 2. Coordinates by Location Name

- **Endpoint:** `/weather/api/get_coordinates/<location_name>/`
- **Method:** GET
- **Description:** Transform any location name or city name into geographical coordinates.
- **Response Format:** JSON
- **Functionality:** 
    - Uses geocoding to find the coordinates for the given location name.
- **Status Codes:**
    - 200: Success, returns coordinates
    - 404: Not Found, e.g., for an invalid location name
- **Example Request:** `/weather/api/get_coordinates/NewYork`

### 3. Other Features

- The project also includes additional features like listing all weather entries and creating new weather entries.

## Directory Structure

- `weather` is the Django project directory.
- `weather/api` contains the API views and serializers.
- `weather/utils` contains utility functions for geocoding and generating random weather data.
- `weather/tests` contains test cases for the API.

## Dockerization (Bonus)

- The project can be Dockerized for easy deployment using a Dockerfile and Docker Compose.

## Usage

To run the project using Docker Compose:

1. Ensure you have Docker and Docker Compose installed on your system.

2. Build the containers:

   ```
   docker-compose build
   ```

3. Start the containers:

   ```
   docker-compose up
   ```

4. You can access the Weather API at `http://localhost:80`.
5. To run `generate_db_entries`, you can use the following command:
   - Run the Docker command:
   ```
   docker-compose run generate_db_entries
   ```

6. To run the tests, you can use the following commands:

   - Run Django tests:
     ```
     docker-compose run test
     ```

   - Run Behave feature tests:
     ```
     docker-compose run behave
     ```

## Docker Compose Services

- **backend**: This service runs the Django application serving the Weather API on port 80. It uses the provided Dockerfile for building the image and sets environment variables from the `.env` file.

- **test**: This service is used to run Django tests for the project. It depends on the `backend` service.

- **behave**: This service is used to run Behave feature tests for the project. It depends on the `backend` service.

Make sure to customize the Docker Compose file and Dockerfile to match your project structure and requirements.

## Testing

- The project includes feature tests that can be run to verify the functionality of the API. 
- These tests are described in the `features` directory in the Weather app.
- The project include testCase using TestCase under weather/tests folder 

## To-Do List

- Remove the SECRET_KEY variable from settings.
- Refactor views to use function-based views to simplify the code.

