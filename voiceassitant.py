import os
import pyttsx3
import json
import logging
import requests
import radio
import asyncio
import ipapi
import urllib.request  
import python_weather
import subprocess
import re
import utils
import alarm
import speech_to_text
import youtubeplayer

trigger_word = "computer"
engine = pyttsx3.Engine()

# speak
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def get_weather():
    # Get the user's location based on their IP address
    url = 'http://ip-api.com/json/'
    response = requests.get(url)
    location_info = json.loads(response.text)

    # Extract relevant location information from API response
    city = location_info['city']
    region = location_info['region']
    country = location_info['country']

    # Use OpenWeatherMap API to get the weather for the user's location
    api_key = 'PUT YOUR API KEY'
    weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city},{region},{country}&appid={api_key}&units=metric'
    response = requests.get(weather_url)
    weather_data = json.loads(response.text)

    # Extract relevant weather information from API response
    description = weather_data['weather'][0]['description']
    temperature = weather_data['main']['temp']
    humidity = weather_data['main']['humidity']
    wind_speed = weather_data['wind']['speed']

    # Print the weather information
    speak(f'The weather in {city} is {description}.')
    speak(f'Temperature: {temperature} celsius')
    speak(f'Humidity: {humidity}%')
    speak(f'Wind speed: {wind_speed} meters per second')

def main():
    #check if internet is working
    if utils.check_if_internet_working():
        pass
    else:
        speak("No internet connection")
        
    while True:
        query = speech_to_text.listen().lower()
        print(query)
        if trigger_word in query or "jervis" in query or "jemmies" in query or "timmy" not in query:
            if "time" in query:
                speak(utils.get_time())
            elif "date" in query:
                speak(utils.get_date())
            elif "stop" in query:
                #os.system("killall chromium-browser")
                os.system("killall vlc")
            elif "radio" in query:
                radio.play_radio("https://streams.ilovemusic.de/iloveradio1.mp3")
            elif "weather" in query:
                get_weather()    
            elif "play" in query:
                speak(youtubeplayer.play_song(query))
            elif "wikipedia" in query or "tell me about" in query or "tell me something about" in query:
                query = query.replace("wikipedia", "")
                query = query.replace("tell me about", "")
                query = query.replace("tell me something about", "")
                speak("Searching...")
                query = query.replace(trigger_word, "")
                speak(utils.get_wikipedia_info(query))
            elif "set an alarm" in query or "set alarm" in query or "set a timer" in query or "set timer" in query:
                speak(alarm.set_alarm(query))
            else:
                print("none")

if __name__ == "__main__":
    main()
