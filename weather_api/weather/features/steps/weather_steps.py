import math
import time
from datetime import datetime

from behave import given, when, then
from rest_framework import status
from rest_framework.test import APIClient

from weather.models import Weather

client = APIClient()
response = None


def is_close(x, y):
    return math.isclose(x, y, rel_tol=1e-3, abs_tol=1e-3)


@given("the application is running")
def step_given_application_running(context):
    pass


@when('I send a GET request to "{url}"')
def step_when_send_get_request(context, url):
    global response
    response = client.get(url)


@then("the response should contain valid weather data")
def step_then_response_contains_valid_weather_data(context):
    assert response.status_code == status.HTTP_200_OK


@then("the response should contain coordinates for New York")
def step_then_response_contains_coordinates_for_new_york(context):
    assert response.status_code == status.HTTP_200_OK
    # Add checks for the response data containing coordinates for New York
    assert 'latitude' in response.json() and 'longitude' in response.json()


@then("the response status code should be {expected_status}")
def step_then_response_status_code(context, expected_status):
    assert response.status_code == int(expected_status)


@then("the response should contain an error message about invalid latitude")
def step_then_response_contains_error_message_about_invalid_latitude(context):
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'latitude' in response.data and 'This field must be a float' in response.data['latitude']


@then("the response should contain an error message about invalid longitude")
def step_then_response_contains_error_message_about_invalid_longitude(context):
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'longitude' in response.data and 'This field must be a float' in response.data['longitude']


@then("the response should contain an error message about latitude and longitude limits")
def step_then_response_contains_error_message_about_coordinates_limits(context):
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'latitude' in response.json()['error']['location']
    assert 'longitude' in response.json()['error']['location']
    assert 'Latitude must be in the range of -90 to 90 degrees.' in response.json()['error']['location']['latitude']
    assert 'Longitude must be in the range of -180 to 180 degrees.' in response.json()['error']['location']['longitude']


@given("there are no weather records for latitude {latitude} and longitude {longitude}")
def step_given_no_weather_records(context, latitude, longitude):
    Weather.objects.filter(location__latitude=latitude, location__longitude=longitude).delete()


@given("there are weather records for latitude {latitude} and longitude {longitude}")
def step_given_weather_records_exist(context, latitude, longitude):
    global response
    latitude = float(latitude)
    longitude = float(longitude)
    response = client.post(f'/weather/api/get_current_weather/{latitude}/{longitude}/')
    weather = response.json()
    context.last_request_json = weather
    assert is_close(weather['location']['latitude'], latitude), f"There is not weather with {latitude}"
    assert is_close(weather['location']['longitude'], longitude), f"There is not weather with {longitude}"


@when('I request current weather data for latitude {latitude} and longitude {longitude}')
def step_when_request_current_weather_data_known(context, latitude, longitude):
    global response
    response = client.get(f'/weather/api/get_current_weather/{latitude}/{longitude}/')
    context.last_request_json = response.json()
    assert context.last_request_json is not None, 'request failed'


@then("I should receive the most recent weather data based on data_timestamp")
def step_then_receive_recent_weather_data(context):
    latitude = context.last_request_json.get('location').get('latitude')
    longitude = context.last_request_json.get('location').get('longitude')

    last_weather = Weather.objects.select_related('location').filter(location__latitude=latitude,
                                                                     location__longitude=longitude).order_by(
        '-data_timestamp').first()
    json_data_timestamp = datetime.fromisoformat(context.last_request_json['data_timestamp'][:-1]).timestamp()
    assert last_weather.data_timestamp.timestamp() == json_data_timestamp, 'different time'


@step('I wait for {second} seconds')
def step_click_button_and_wait(context, second):
    # Realiza la acción de hacer clic en el botón
    # Espera 2 segundos
    time.sleep(int(second))


@then(u'I should receive random weather data')
def step_impl(context):
    pass
