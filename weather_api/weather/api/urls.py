from django.urls import path, register_converter
from weather.api import views
from ..converter import FloatConverter

register_converter(FloatConverter, 'float')

urlpatterns = [
    path(
        'api/get_current_weather/<float:latitude>/<float:longitude>/',
        views.CurrentWeather.as_view(),
        name='get-current-weather'
    ),
    path('api/get_coordinates/<str:location_name>', views.CoordinatesByLocation.as_view(), name='get-coordinates'),
    path('api/', views.WeatherList.as_view(), name='weather-list'),
    path('api/<int:pk>/', views.WeatherDetail.as_view(), name='weather-detail'),
    path('api/total/', views.WeatherTotalView.as_view(), name='total-weather'),
]
