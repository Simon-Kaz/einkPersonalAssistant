from datetime import datetime, timedelta
from time import strftime
from decouple import config
import requests, json

# constants
API_URL = "https://api.tomorrow.io/v4/timelines"
API_KEY = config('tomorrowAPIKey')
HEADERS = {"Accept": "application/json"}
LOCATION_ID = "620678a05eca870007bde691"
TIMESTAMP_FORMAT ='%Y-%m-%dT%H:%M:%SZ'


fields = [
  "precipitationIntensity",
  "precipitationType",
  "windSpeed",
  "windGust",
  "temperature",
  "temperatureApparent",
  "cloudCover",
  "weatherCode"
]

units = "metric"
timesteps = ["current"]

now = datetime.utcnow()
startTime = now.strftime(TIMESTAMP_FORMAT)
endTime = (now + timedelta(days=1)).strftime(TIMESTAMP_FORMAT)
timezone = "Eire"

def main():

    # GET DAILY FORECAST
    dayRequestUrl = API_URL + '?' + 'location=' + LOCATION_ID +'&units=' + units + '&fields=' + '&fields=weatherCodeFullDay&fields=sunriseTime&fields=sunsetTime' + '&timesteps=1d' + "&startTime=" + startTime + "&endTime=" + endTime + '&apikey=' + API_KEY
    dayResponse = requests.request("GET", dayRequestUrl, headers=HEADERS)  
    dayResponseJson = json.loads(dayResponse.text)
    print(dayResponseJson)
    print("######################")
    # GET CURRENT WEATHER FORECAST 
    currentRequestUrl = API_URL + '?' + 'location=' + LOCATION_ID +'&units=' + units + '&fields=' + '&fields='.join(fields) + '&timesteps=' + '&timesteps='.join(timesteps) + '&apikey=' + API_KEY
    response = requests.request("GET", currentRequestUrl, headers=HEADERS)  
    responseJson = json.loads(response.text)
    print(responseJson)
  
    dayData = dayResponseJson['data']['timelines'][0]['intervals'][0]['values']
    data = responseJson['data']['timelines'][0]['intervals'][0]['values']
    # wind speed
    print("Wind Speed: " + str(data['windSpeed']) + "km/h")
    print("Gust: " + str(data['windGust']) + "km/h")
    #temperature
    print("Temperature: " + str(data['temperature']) + "°C")
    # `Feels Like` temperature
    print("Feels Like: " + str(data['temperatureApparent']) + "°C")
    # Cloud cover
    print("Cloud Coverage: " + str(data['cloudCover']) + "%")
    
    #precipitation
    print("Precipitation: " + str(data['precipitationIntensity']) + "mm/hr")
    print("Type: " + getPrecipitationType(data['precipitationType']))

    # convert weather code to string representation
    print("Weather Code: " + getWeatherFromCode(data['weatherCode']))

    # get sunrise/sunset values 
    sunriseTime = datetime.strptime(dayData['sunriseTime'], TIMESTAMP_FORMAT).strftime("%H:%M")
    sunsetTime = datetime.strptime(dayData['sunsetTime'], TIMESTAMP_FORMAT).strftime("%H:%M")
    print("Sunrise: " + sunriseTime)
    print("Sunset: " + sunsetTime)

def getPrecipitationType(code):
  match code:
    case 0:
      return "N/A"
    case 1:
      return "Rain"
    case 2:
      return "Snow"
    case 3:
      return "Freezing Rain"
    case 4:
      return "Ice Pellets / Sleet"



def getWeatherFromCode(code):
  match code:
    case 0:
      return "Unknown"
    case 1000:
      return "Clear"
    case 1001:
       return "Cloudy"
    case 1100:
      return "Mostly Clear"
    case 1101:
      return "Partly Cloudy",
    case 1102: 
        return "Mostly Cloudy"
    case 2000: 
      return "Fog"
    case 2100: 
      return "Light Fog"
    case 3000: 
      return "Light Wind"
    case 3001: 
      return "Wind"
    case 3002: 
      return "Strong Wind"
    case 4000: 
      return "Drizzle"
    case 4001: 
      return "Rain"
    case 4200: 
      return "Light Rain"
    case 4201: 
      return "Heavy Rain"
    case 5000: 
      return "Snow"
    case 5001: 
      return "Flurries"
    case 5100: 
      return "Light Snow"
    case 5101: 
      return "Heavy Snow"
    case 6000: 
      return "Freezing Drizzle"
    case 6001: 
      return "Freezing Rain"
    case 6200: 
      return "Light Freezing Rain"
    case 6201: 
      return "Heavy Freezing Rain"
    case 7000: 
      return "Ice Pellets"
    case 7101: 
      return "Heavy Ice Pellets"
    case 7102: 
      return "Light Ice Pellets"
    case 8000: 
      return "Thunderstorm"

if __name__ == '__main__':
    main()