import requests
from requests.exceptions import HTTPError, Timeout, RequestException

Locations = {'Ridgefield, WA' : '45.80916343 -122.72333044',
            'Hillsboro, OR' : '45.522896 -122.989830',
            'Santa Clara, CA' : '37.35411 -121.95524'
            #'Bengaluru, KA' : '12.971599 77.594566'
            }
def make_nws_request(endpoint, user_agent):
    headers = {
        "User-Agent": user_agent
    }

    try:
        response = requests.get(
                       endpoint, 
                       headers=headers
                   )
        # Raise HTTPError for bad responses (4xx or 5xx)
        response.raise_for_status()
        return response.json()

    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} - Status code: {response.status_code}")
    except Timeout as timeout_err:
        print(f"Request timed out: {timeout_err}")
    except RequestException as req_err:
        print(f"Request error: {req_err}")
    
    return None  # Return None if an error occurred

def get_current_gridInfo():
    office = data['properties']['gridId']
    grid_x = data['properties']['gridX']
    grid_y = data['properties']['gridY']
    #print(f"Forecast in City: {city_disp}, Grid X: {grid_x}, Grid Y: {grid_y}")
    return(office, grid_x, grid_y)

def get_temp_update(City, gridID, gridX, gridY, user_agent):
    headers = {"User-Agent": user_agent}
    hourly_forecast_url = f"https://api.weather.gov/gridpoints/{gridID}/{gridX},{gridY}/forecast/hourly"
    hourly_forecast_response = requests.get(hourly_forecast_url, headers=headers).json()
    #print(hourly_forecast_response)
    
  # The current temperature is typically found in the first period of the hourly forecast
    current_period = hourly_forecast_response['properties']['periods'][0]
    current_temperature = current_period['temperature']
    current_temperature_celsius = round((current_temperature - 32) * 5/9,1)
    temperature_unit = current_period['temperatureUnit']

    print(f"Current Temp in {City} is: {current_temperature_celsius}° Celsius")


if __name__ == "__main__":

    user_agent = "MyWeatherApp/1.0 (hssbme@gmail.com)"

    BASE_URL = "https://api.weather.gov"
    
    for City in Locations:
        lat, lon = Locations[City].split()
        forecast_url = f"{BASE_URL}/points/{lat},{lon}"
        data = make_nws_request(forecast_url, user_agent)
        
        if data:
    
            #print(data)
            gridID, gridX, gridY = get_current_gridInfo()
            #print(gridID, gridX, gridY)
            get_temp_update(City, gridID, gridX, gridY, user_agent)
            
        else:
            print("Failed to retrieve data.")
            
         