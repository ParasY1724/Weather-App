from django.shortcuts import render
import requests
import datetime

def index(request):
    api_key = '2590d6c88bbf9787d94ed4b4e30767ce'
    current_weather_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
    forecast_url = 'https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}'

    if request.method == 'POST':
        city1 = request.POST['city1']

        if city1:
            weather_data1, daily_forecasts1 = fetch_weather_and_forecast(city1, api_key, current_weather_url,forecast_url)
        else:
            weather_data1, daily_forecasts1 = None, None

        context = {
            'weather_data1': weather_data1,
            'daily_forecasts1': daily_forecasts1,
        }
        return render(request, 'Weather.html', context)
    
    else:
        return render(request, 'Weather.html')


def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
    response = requests.get(current_weather_url.format(city, api_key)).json()
    lat, lon = response['coord']['lat'], response['coord']['lon']
    forecast_response = requests.get(forecast_url.format(lat, lon, api_key)).json()

    weather_data = {
        'city': str(city).upper(),
        'temperature': round(response['main']['temp'] - 273.15, 2),
        'description': response['weather'][0]['description'],
        'humidity':round(response['main']['humidity'],2),
        'pressure':response['main']['pressure'],
        'wind':response['wind']['speed'],
        'icon': response['weather'][0]['icon'],
    }

    temp_day=""
    daily_forecasts = []
    for daily_data in forecast_response['list'][:]:
        if (temp_day != datetime.datetime.fromtimestamp(daily_data['dt']).strftime('%A')):
            temp_day=datetime.datetime.fromtimestamp(daily_data['dt']).strftime('%A')
            daily_forecasts.append({
            'day': temp_day,
            'min_temp': round(daily_data['main']['temp_min'] - 273.15, 2),
            'max_temp': round(daily_data['main']['temp_max'] - 273.15, 2),
            'description': daily_data['weather'][0]['description'],
            'date': ((daily_data['dt_txt']).split())[0],
            'time': ((daily_data['dt_txt']).split())[1],
            'icon': daily_data['weather'][0]['icon'],
        })
        if (len(daily_forecasts)==5) :
            break; 
        

    return weather_data, daily_forecasts
