from rest_framework import serializers

from .models import Location, Weather


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class WeatherSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    
    class Meta:
        model = Weather
        fields = '__all__'

    def __init__(self, geocoder_instance=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geocoder = geocoder_instance

    def create(self, validated_data):
        # Extract the location from the validated data
        location_data = validated_data.pop('location')

        # Use the geocoder to search for the location
        location_info = self.geocoder.geocode_from_location_name(location_data["name"])

        if location_info:
            # Create a new Weather instance with the found location
            weather = Weather.objects.create(location=location_info, **validated_data)
            return weather
        else:
            # Handle the case where the location cannot be found
            raise serializers.ValidationError("Location could not be found")
