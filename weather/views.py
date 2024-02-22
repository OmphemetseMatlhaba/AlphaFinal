from datetime import datetime, timedelta
import os
from django.shortcuts import redirect, render
import requests
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import FarmInfo

api_key = 'a1aea166811f4436b42195f0b982052e'

# Create your views here.
def main(request):
    user = request.user 
    latitude_input = request.POST.get('latitudeInput')
    longitude_input = request.POST.get('longitudeInput')

    if longitude_input and latitude_input:
        lat = latitude_input
        lon = longitude_input
    else:
        if user.is_authenticated:
            try:
                farm_info = user.farm_info.get()
                if farm_info.info_filled:
                    lon = farm_info.longitude
                    lat = farm_info.latitude
                else:
                    messages.info('Please complete your profile')
                    return redirect('farm_info')
            except ObjectDoesNotExist:
                lat = -25.7313
                lon = 28.218370
        else:
            lat = -25.7313
            lon = 28.218370
        
    current_url = f'https://api.weatherbit.io/v2.0/current?lat={lat}&lon={lon}&key={api_key}&units=metric'
    response = requests.get(current_url)
    weather_data = response.json()

    current_date = datetime.now().strftime('%A')
    wind_speed = weather_data['data'][0]['wind_spd']
    pressure = weather_data['data'][0]['pres']
    cloud_coverage = weather_data['data'][0]['clouds']
    temperature = weather_data['data'][0]['temp']
    description = weather_data['data'][0]['weather']['description']
    code = weather_data['data'][0]['weather']['code']
    city = weather_data['data'][0]['city_name']
    observe = weather_data['data'][0]['ob_time'] 
    current_day = weather_data['data'][0]

    hourly_url = f'https://api.weatherbit.io/v2.0/forecast/daily?lat={lat}&lon={lon}&key={api_key}&days=5'
    hourly_response = requests.get(hourly_url)
    five_day_data = hourly_response.json()

    secondary_url = f'https://api.weatherbit.io/v2.0/forecast/hourly?lat={lat}&lon={lon}&key={api_key}&hours=24'
    hour = requests.get(secondary_url)
    hourly_data = hour.json()

    third_url = f'https://api.weatherbit.io/v2.0/current/airquality?lat={lat}&lon={lon}&key={api_key}'
    quality_response = requests.get(third_url)
    air_quality = quality_response.json()

    fourth_url = f'https://api.weatherbit.io/v2.0/forecast/agweather?lat={lat}&lon={lon}&key={api_key}'
    agri_response = requests.get(fourth_url)
    agris = agri_response.json()

    
    context = {

        'current_date': current_date,
        'wind_speed': wind_speed,
        'pressure': pressure,
        'cloud_coverage': cloud_coverage,
        'temperature': temperature,
        'description': description,
        'observe': observe,
        'code': code,
        'city': city,
        'five_day_data': five_day_data,
        'current_day': current_day,
        'hourly_data': hourly_data,
        'lat': lat,
        'lon': lon,
        'air_quality' : air_quality,
        'agris': agris
    }
    if request.user.is_authenticated:
        context['profile_picture'] = user.profile.profile_picture
        
    return render(request, 'weather/main.html', context)

def past_weather_data(request, lat, lon):
    latitude = lat
    longitude = lon
    today = datetime.now()
    start_date_raw = today - timedelta(days=7)
    start_date_input = request.POST.get('start_date')
    end_date_input= request.POST.get('end_date')
    
    if start_date_input is not None and end_date_input is not None:
        start_date = start_date_input
        end_date = end_date_input
    else:
        start_date = start_date_raw.strftime('%Y-%m-%d')
        end_date = today.strftime('%Y-%m-%d')

    past_data_url = f'https://api.weatherbit.io/v2.0/history/daily?lat={latitude}&lon={longitude}&start_date={start_date}&end_date={end_date}&key={api_key}'
    past = requests.get(past_data_url)
    past_data = past.json()

    
    context = {
        'longitude': longitude,
        'latitude' : latitude,
        'past_data': past_data,
        'start_date': start_date,
        'end_date': end_date,
    }
    if request.user.is_authenticated:
        context['profile_picture'] = request.user.profile.profile_picture
    return render(request, 'weather/past_weather.html', context)

def past_air_quality(request, lat, lon):
    latitude = lat
    longitude = lon
    today = datetime.now()
    start_date_raw = today - timedelta(days=2)
    start_date_input = request.POST.get('start_date')
    end_date_input= request.POST.get('end_date')
    
    if start_date_input is not None and end_date_input is not None:
        start_date = start_date_input
        end_date = end_date_input
    else:
        start_date = start_date_raw.strftime('%Y-%m-%d')
        end_date = today.strftime('%Y-%m-%d')

    air_quality_url = f'https://api.weatherbit.io/v2.0/history/airquality?lat={latitude}&lon={longitude}&start_date={start_date}&end_date={end_date}&key={api_key}'
    air_qual_response = requests.get(air_quality_url)
    air_quality = air_qual_response.json()

    context = {
        'latitude': latitude,
        'longitude': longitude,
        'start_date': start_date,
        'end_date': end_date,
        'air_quality': air_quality,
    }
    if request.user.is_authenticated:
        context['profile_picture'] = request.user.profile.profile_picture
    return render(request, 'weather/past_air_quality.html', context)

def past_agri_weather(request, lat, lon):
    latitude = lat
    longitude = lon

    today = datetime.now()
    start_date_raw = today - timedelta(days=7)
    start_date_input = request.POST.get('start_date')
    end_date_input= request.POST.get('end_date')
    
    if start_date_input is not None and end_date_input is not None:
        start_date = start_date_input
        end_date = end_date_input
    else:
        start_date = start_date_raw.strftime('%Y-%m-%d')
        end_date = today.strftime('%Y-%m-%d')
    
    ag_weather_url = f'https://api.weatherbit.io/v2.0/history/agweather?lat={latitude}&lon={longitude}&start_date={start_date}&end_date={end_date}&key={api_key}'
    ag_weather_response = requests.get(ag_weather_url)
    ag_weather = ag_weather_response.json()
   
    context = {
        'latitude': latitude,
        'longitude': longitude,
        'start_date': start_date,
        'end_date': end_date,
        'ag_weather': ag_weather
    }
    if request.user.is_authenticated:
        context['profile_picture'] = request.user.profile.profile_picture
    return render(request, 'weather/past_agri_weather.html', context)


def future_agri_weather(request, lat, lon):
    latitude = lat
    longitude = lon

    today = datetime.now()
    start_date = today.strftime('%Y-%m-%d')
    
    end_date_raw = today + timedelta(days=8)
    end_date = end_date_raw.strftime('%Y-%m-%d')
    
    ag_weather_url = f'https://api.weatherbit.io/v2.0/forecast/agweather?lat={latitude}&lon={longitude}&key={api_key}'
    ag_weather_response = requests.get(ag_weather_url)
    ag_weather = ag_weather_response.json()

    context = {
        'latitude': latitude,
        'longitude': longitude,
        'start_date': start_date,
        'end_date': end_date,
        'ag_weather': ag_weather
    }
    if request.user.is_authenticated:
        context['profile_picture'] = request.user.profile.profile_picture
    return render(request, 'weather/future_agric_weather.html', context)

def future_weather_daily(request, lat, lon):
    latitude = lat
    longitude = lon
    today = datetime.now()
    start_date = today.strftime('%Y-%m-%d')
    
    end_date_raw = today + timedelta(days=16)
    end_date = end_date_raw.strftime('%Y-%m-%d')
    day_input = request.POST.get('number_of_days')

    if day_input is not None and request.method == 'POST':
        days = day_input
    else:
        days = 7

    past_data_url = f'https://api.weatherbit.io/v2.0/forecast/daily?lat={latitude}&lon={longitude}&key={api_key}&days={days}'
    past = requests.get(past_data_url)
    future_data = past.json()

    context = {
        'longitude': longitude,
        'latitude' : latitude,
        'future_data': future_data,
        'start_date': start_date,
        'end_date': end_date,
        'days': days,
    }
    if request.user.is_authenticated:
        context['profile_picture'] = request.user.profile.profile_picture
    return render(request, 'weather/future_daily_weather.html', context)