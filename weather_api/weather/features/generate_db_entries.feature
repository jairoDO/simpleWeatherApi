Feature: Testing Weather Command and View

  Scenario: Generate and view Weather entries
    Given I get the current total count from WeatherTotalView
    When I run the Weather generation command with count 5
    And I make a GET request to the WeatherTotalView endpoint
    Then the new total count should be 5 greater than the previous total count