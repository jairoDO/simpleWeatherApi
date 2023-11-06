from rest_framework import serializers
from ..models import Location, Weather


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class WeatherSerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta:
        model = Weather
        fields = '__all__'

    def create(self, validated_data):
        location_data = validated_data.pop('location')
        location, created = Location.objects.get_or_create(**location_data)
        weather = Weather.objects.create(location=location, **validated_data)
        return weather
