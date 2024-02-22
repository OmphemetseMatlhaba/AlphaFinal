from django.urls import path
from weather import views

urlpatterns = [
    path('', views.main, name='weather'),
    path('past_data/<str:lat>_<str:lon>', views.past_weather_data, name='past_weather_data'),
    path('past_air_quality/<str:lat>_<str:lon>', views.past_air_quality, name='past_air_quality'),
    path('past_agric_weather/<str:lat>_<str:lon>', views.past_agri_weather, name='past_agric_weather'),
    path('future_agric_weather/<str:lat>_<str:lon>', views.future_agri_weather, name='future_agric_weather'),
    path('future_weather_daily/<str:lat>_<str:lon>', views.future_weather_daily, name='future_weather_daily'),
]