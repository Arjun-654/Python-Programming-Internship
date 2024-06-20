import requests
import matplotlib.pyplot as plt
import datetime

# Function to fetch current weather data from Open-Meteo API
def fetch_weather_data(lat, lon):
    current_weather_url = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true'
    forecast_url = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m&daily=temperature_2m_max,temperature_2m_min&timezone=auto'
    
    current_weather_response = requests.get(current_weather_url)
    current_weather_response.raise_for_status()  # Raise an exception for HTTP errors
    
    forecast_response = requests.get(forecast_url)
    forecast_response.raise_for_status()  # Raise an exception for HTTP errors
    
    return current_weather_response.json(), forecast_response.json()

# Function to display current weather data
def display_current_weather(weather_data):
    current_weather = weather_data['current_weather']
    print("Current weather:")
    print(f"Temperature: {current_weather['temperature']}°C")
    print(f"Windspeed: {current_weather['windspeed']} km/h")
    print(f"Wind direction: {current_weather['winddirection']}°")
    print()

# Function to display forecast data
def display_forecast(forecast_data):
    daily_forecast = forecast_data['daily']
    dates = daily_forecast['time']
    max_temps = daily_forecast['temperature_2m_max']
    min_temps = daily_forecast['temperature_2m_min']
    
    print("5-day forecast:")
    for date, max_temp, min_temp in zip(dates, max_temps, min_temps):
        print(f"{date}: Max Temp: {max_temp}°C, Min Temp: {min_temp}°C")
    print()

# Function to parse datetime with optional seconds
def parse_datetime(date_str):
    for fmt in ('%Y-%m-%dT%H:%M:%S', '%Y-%m-%dT%H:%M'):
        try:
            return datetime.datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"Date format for '{date_str}' not recognized")

# Function to plot temperature trends
def plot_temperature_trends(forecast_data):
    hourly_forecast = forecast_data['hourly']
    times = hourly_forecast['time']
    temperatures = hourly_forecast['temperature_2m']
    
    dates = [parse_datetime(time) for time in times]
    
    plt.figure(figsize=(10, 5))
    plt.plot(dates, temperatures, marker='o')
    plt.title('Temperature Trends')
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.grid(True)
    plt.show()

# Function to get latitude and longitude from user input
def get_location_coordinates(location):
    geocoding_url = f'https://geocoding-api.open-meteo.com/v1/search?name={location}'
    response = requests.get(geocoding_url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    
    data = response.json()
    if data['results']:
        return data['results'][0]['latitude'], data['results'][0]['longitude']
    else:
        raise ValueError("Location not found")

# Main function to fetch and display weather data
def main():
    location = input("Enter the location (e.g., London): ")
    try:
        lat, lon = get_location_coordinates(location)
        current_weather, forecast = fetch_weather_data(lat, lon)
        
        display_current_weather(current_weather)
        display_forecast(forecast)
        plot_temperature_trends(forecast)
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except ValueError as val_err:
        print(f"Error: {val_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

if __name__ == "__main__":
    main()
