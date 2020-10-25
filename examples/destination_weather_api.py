#!/usr/bin/env python

from herepy import DestinationWeatherApi, WeatherProductType

destination_weather_api = DestinationWeatherApi("api_key")

# weather conditions with given location name
response = destination_weather_api.weather_for_location_name(
    location_name="Berlin", product=WeatherProductType.forecast_7days
)
print(response.as_dict())

# weather conditions within given coordinates
response = destination_weather_api.weather_for_coordinates(
    latitude=52.51784,
    longitude=13.38736,
    product=WeatherProductType.forecast_7days,
)
print(response.as_dict())

# weather conditions within given zipcode
response = destination_weather_api.weather_for_zip_code(
    zip_code="10025", product=WeatherProductType.forecast_7days
)
print(response.as_dict())
