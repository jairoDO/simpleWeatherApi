# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Location, Weather


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'country', 'name', 'latitude', 'longitude')
    search_fields = ('name',)


@admin.register(Weather)
class WeatherAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'temperature',
        'condition',
        'pressure',
        'humidity',
        'sea_level',
        'ground_level',
        'visibility',
        'wind_speed',
        'wind_direction',
        'clouds',
        'rain_1h',
        'data_timestamp',
        'timezone',
        'sunrise',
        'sunset',
        'location',
    )
    list_filter = ('data_timestamp', 'sunrise', 'sunset', 'location')
