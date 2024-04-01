import requests
import json


def get_cities(city_name):
    base_url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": city_name,
        "count": 10,
        "format": "json",
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()

        if response.json()["results"]:
            return response.json()["results"]
        else:
            print("No matching locations found for", city_name)
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None


def get_city_data(cities):
    if not isinstance(cities, (list, dict)):
        raise TypeError("Input 'cities' must be a list or a dictionary.")

    city_data = []

    if isinstance(cities, list):
        for city in cities:
            city_info = {
                "id": city.get("id", ""),
                "name": city.get("name", ""),
                "timezone": city.get("timezone", ""),
                "lat": city.get("latitude", ""),
                "long": city.get("longitude", ""),
                "country_code": city.get("country_code", ""),
            }
            city_data.append(city_info)
        else:
            return city_data


def get_forecast(lat, long):
    base_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": long,
        "hourly": ["temperature_2m", "precipitation", "windspeed_10m"],
        "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum"],
        "forecast_days": 1
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()

        data = response.json()

        if isinstance(data, list):
            print("Multiple locations found. Processing the first location...")
            data = data[0]
        return data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")


def main():
    # testing
    data = get_cities(str(input(">")))
    print("="*100)
    c = get_city_data(data)
    for index, city in enumerate(c):
        print(index, city)

    print("="*100)
    choice = int(input("> "))
    lat = c[choice]['lat']
    long = c[choice]['long']
    print("="*100)

    print(json.dumps(get_forecast(lat, long), indent=4))


if __name__ == "__main__":
    main()
