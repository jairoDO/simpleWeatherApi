Feature: Weather API

  Background:
    Given the application is running

  Scenario: Get current weather data by latitude and longitude
    When I send a GET request to "/weather/api/get_current_weather/61.999/66.3581/"
    Then the response status code should be 200
    And the response should contain valid weather data

  Scenario: Get current weather data with invalid latitude and longitude
    When I send a GET request to "/weather/api/get_coordinates/invalid_latitude/invalid_longitude/"
    Then the response status code should be 404

  Scenario: Get coordinates by location name
    When I send a GET request to "/weather/api/get_coordinates/NewYork"
    Then the response status code should be 200
    And the response should contain coordinates for New York

  Scenario: Get coordinates by invalid location name
    When I send a GET request to "/weather/api/get_coordinates/InvalidLocation/"
    Then the response status code should be 404

  Scenario: Get current weather data with latitude and longitude exceeding limits
    When I send a GET request to "/weather/api/get_current_weather/1000/2000/"
    Then the response status code should be 400
    And the response should contain an error message about latitude and longitude limits

  Scenario: Retrieving current weather data with unknown latitude and longitude
    Given there are no weather records for latitude 18.1535858 and longitude -74.0060
    When I request current weather data for latitude 40.7128 and longitude -74.0060
    Then the response status code should be 400
  
  
  Scenario: Retrieving current weather data with known latitude and longitude
    Given there are weather records for latitude 61.999 and longitude 66.3581
    And I wait for 2 seconds
    And there are weather records for latitude 61.999 and longitude 66.3581
    When I request current weather data for latitude 61.999 and longitude 66.3581
    Then I should receive the most recent weather data based on data_timestamp
  