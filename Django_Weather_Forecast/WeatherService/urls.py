from django.urls import path
from WeatherService import views

urlpatterns = [ 
    path('currentWeather/',views.currentWeather.as_view()),
    path('currentWeatherChart/',views.currentWeatherChart.as_view()),
    path('forecastWeather/',views.forecastWeather.as_view())
]