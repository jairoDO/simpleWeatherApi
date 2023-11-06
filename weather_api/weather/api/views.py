from django.http import Http404, JsonResponse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import WeatherSerializer
from ..models import Weather
from ..utils.geocoder import Geocoder
from ..validators import validate_coordinates

geocoder = Geocoder()


class CoordinatesByLocation(APIView):
    @staticmethod
    def get(request, location_name):
        if location_name:
            # Utilize geopy to perform reverse geocoding
            coordinates = geocoder.geocode_from_location_name(location_name)

            if coordinates:
                return Response(coordinates, status=status.HTTP_200_OK)

        return JsonResponse({"error": "Invalid parameters"}, status=status.HTTP_404_NOT_FOUND)


class CurrentWeather(APIView):

    @validate_coordinates
    def get(self, request, latitude, longitude):
        # looking the nearest weather record
        location = geocoder.reverse_geocode(latitude, longitude)
        latitude, longitude = location.get('latitude'), location.get('longitude')
        nearest_weather = Weather.objects.select_related('location').filter(
            location__latitude=latitude, location__longitude=longitude
        ).order_by('-data_timestamp').first()

        if nearest_weather:
            return Response(WeatherSerializer(nearest_weather).data, status=status.HTTP_200_OK)

        location_data = geocoder.reverse_geocode(longitude, latitude)
        if 'error' in location_data:
            return Response({'error': 'Location not found'}, status=status.HTTP_400_BAD_REQUEST)
        
        # if we didn't find any we will created a new weather with random data.
        new_weather = Weather.generate_random_weather_with_real_location(
            geocoder_instance=geocoder,
            location_data=location_data
            
            )

        serializer = WeatherSerializer(data=new_weather)

        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    @validate_coordinates
    def post(self, request, latitude, longitude):
        location_data = geocoder.reverse_geocode(latitude, longitude)
        if 'error' in location_data:
            return Response({'error': 'Location not found'}, status=status.HTTP_400_BAD_REQUEST)
       
        new_weather = Weather.generate_random_weather_with_real_location(
            geocoder_instance=geocoder,
            location_data=location_data
            )
        serializer = WeatherSerializer(data=new_weather)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class WeatherList(APIView):
    """
    List all Weather entries or create a new one.
    """
    @staticmethod
    def get(request):
        weather_entries = Weather.objects.all()
        serializer = WeatherSerializer(weather_entries, many=True)
        return Response(serializer.data)


class WeatherDetail(APIView):
    """
    Retrieve, update or delete a Weather entry.
    """
    @staticmethod
    def get_object(pk):
        try:
            return Weather.objects.get(pk=pk)
        except Weather.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        weather_entry = self.get_object(pk)
        serializer = WeatherSerializer(weather_entry)
        return Response(serializer.data)

    def put(self, request, pk):
        weather_entry = self.get_object(pk)
        serializer = WeatherSerializer(weather_entry, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        weather_entry = self.get_object(pk)
        weather_entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WeatherTotalView(APIView):
    @staticmethod
    def get(request):
        total_count = Weather.objects.count()
        return Response({"total_count": total_count})
