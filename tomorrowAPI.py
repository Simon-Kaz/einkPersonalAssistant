from datetime import datetime, timedelta
import requests
import json
import os

apiUrl = "https://api.tomorrow.io/v4/timelines"
apiKey = os.environ['tomorrowAPIKey']
locationId = "620678a05eca870007bde691"
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

now = datetime.now()
startTime = now.isoformat()
endTime = (now + timedelta(days=1)).isoformat()

timezone = "Eire"


def main():
    requestUrl = apiUrl + '?' + 'location=' + locationId +'&units=' + units + '&fields=' + '&fields='.join(fields) + '&timesteps=' + '&timesteps='.join(timesteps) + '&apikey=' + apiKey
    headers = {"Accept": "application/json"}
    print(requestUrl)
    response = requests.request("GET", requestUrl, headers=headers)  
    responseJson = json.loads(response.text)
    print(responseJson)
  
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