from behave import given, when, then
from django.core.management import call_command
from rest_framework.test import APIClient

client = APIClient()
# Variable to store the previous total count before generation
previous_total_count = 0


@given('I get the current total count from WeatherTotalView')
def get_current_total_count(context):
    global previous_total_count
    response = client.get('/weather/api/total/')
    previous_total_count = response.data['total_count']


@when('I run the Weather generation command with count {count:d}')
def run_weather_generation_command(context, count):
    call_command('generate_db_entries', f'--count={count}')


@when('I make a GET request to the WeatherTotalView endpoint')
def make_get_request_to_weather_total_view(context):
    context.response = client.get('/weather/api/total/')


@then('the new total count should be {count:d} greater than the previous total count')
def assert_new_total_count(context, count):
    global previous_total_count
    response_data = context.response.data
    new_total_count = response_data['total_count']
    assert new_total_count == previous_total_count + count,\
        f'New total count is not {count} greater than the previous total count'
