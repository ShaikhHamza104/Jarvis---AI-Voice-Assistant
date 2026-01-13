import pyttsx3
import speech_recognition as sr
import webbrowser as web
from datetime import datetime
from typing import Dict, Optional
from openai import OpenAI
from dotenv import load_dotenv
import requests
import os
import time

# Dictionary of websites
Site: Dict[str, str] = {
    "youtube": 'https://www.youtube.com/',
    "google": 'https://www.google.com/', 
    "github": 'https://www.github.com/ShaikhHamza104',
    "stackoverflow": 'https://stackoverflow.com/',
    "gmail": 'https://mail.google.com/',
    "wikipedia": 'https://www.wikipedia.org/'
}

def get_weather(city_name: str) -> str:
    """Fetch weather information for a city using OpenWeather API."""
    try:
        load_dotenv()
        api_key: Optional[str] = os.getenv("OPEN_WEATHER_API_KEY")
        
        if not api_key:
            return "Error: OPEN_WEATHER_API_KEY not found in environment variables."
        
        # OpenWeather API endpoint
        url: str = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
        
        response: requests.Response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise exception for bad status codes
        
        data: dict = response.json()
        
        if response.status_code == 200:
            temperature: float = data['main']['temp']
            weather_description: str = data['weather'][0]['description']
            humidity: int = data['main']['humidity']
            wind_speed: float = data['wind']['speed']
            
            weather_info: str = (f"The weather in {city_name} is {temperature}°C with "
                                 f"{weather_description.capitalize()}. Humidity is {humidity}% "
                                 f"and wind speed is {wind_speed} m/s.")
            return weather_info
        else:
            return f"Unable to fetch weather for {city_name}."
            
    except requests.exceptions.ConnectionError:
        return "Connection error. Unable to reach weather service."
    except requests.exceptions.Timeout:
        return "Request timeout. Please try again."
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return f"City '{city_name}' not found. Please check the spelling."
        else:
            return f"Error fetching weather: {e}"
    except Exception as e:
        return f"Unable to fetch weather data for {city_name}. Error: {str(e)}"

def get_ai_response(user_query: str) -> Optional[str]:
    """Get AI response using OpenRouter API with GPT-3.5 Turbo model."""
    try:
        load_dotenv()
        api_key: Optional[str] = os.getenv("OPEN_ROUTER_API_KEY")
        
        if not api_key:
            return "API key not found."
        
        client: OpenAI = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1",
        )
        
        response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_query}],
            max_tokens=50,
            temperature=0.5,
        )
        
        return response.choices[0].message.content if response.choices else None
            
    except Exception as e:
        print(f"AI Error: {e}")
        return "I'm having trouble right now. Try again."

def open_website(site_name: str) -> None:
    """Open a website in the default browser."""
    try:
        web.open(Site[site_name])
        say_text(f"Opening {site_name}")
    except KeyError:
        say_text(f"Website {site_name} not found in the list.")

def water_reminder() -> None:
    """Remind the user to drink water every hour."""
    while True:
        time.sleep(3600)  # Sleep for 1 hour
        say_text("It's time to drink water. Stay hydrated!")

def wish_me() -> None:
    """Greet the user based on the current time of day."""
    hour: int = datetime.now().hour
    if 0 <= hour < 12:
        say_text("Good Morning!")
    elif 12 <= hour < 18:
        say_text("Good Afternoon!")
    else:
        say_text("Good Evening!")

def say_text(text: str) -> None:
    """Convert text to speech and speak it aloud."""
    try:
        engine: pyttsx3.Engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error speaking text: {e}")

def take_command() -> str:
    """Listen to user's voice input and convert it to text using Google Speech Recognition."""
    recognizer: sr.Recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.pause_threshold = 1
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio: sr.AudioData = recognizer.listen(source)
        
        command: str = recognizer.recognize_google(audio).lower()
        print(f"User said: {command}")
        return command
        
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return ""

def process_command(command: str) -> bool:
    """Process user voice commands and execute appropriate actions."""
    if not command:
        return True
    
    print(f"Recognized command: {command}")
    
    if command == "stop":
        say_text("Stopping Jarvis. Goodbye!")
        return False
    
    elif "open" in command:
        site_name: str = command.replace("open", "").strip()
        site_name = site_name.split()[0] if site_name else ""
        open_website(site_name)
    
    elif "date" in command:
        date_str: str = datetime.now().strftime("%d-%m-%Y")
        say_text(f"Today's date is {date_str}")
    
    elif "time" in command:
        time_str: str = datetime.now().strftime("%H:%M:%S")
        say_text(f"The time is {time_str}")
    
    elif "weather" in command:
        if "weather in" in command:
            city_name: str = command.replace("weather in", "").strip()
        else:
            city_name: str = command.replace("weather", "").strip()
        
        if not city_name:
            say_text("Which city would you like to know the weather for?")
            city_name = take_command().strip()
            if not city_name:
                say_text("I didn't catch the city name. Please try again.")
                return True
        
        weather_info: str = get_weather(city_name)
        say_text(weather_info)
    
    elif "ai" in command:
        ai_response: Optional[str] = get_ai_response(command)
        say_text(ai_response if ai_response else "I couldn't get a response from the AI.")
    
    else:
        say_text("I did not understand that command.")
    
    return True

def main() -> None:
    """Initialize and run Jarvis voice assistant."""
    print("Jarvis is ready. Say 'start' to activate...")
    say_text("Jarvis is ready. Say start to activate.")
    
    # Start water reminder in a separate thread
    import threading
    reminder_thread = threading.Thread(target=water_reminder, daemon=True)
    reminder_thread.start()
    
    # Wait for start command
    while True:
        command: str = take_command()
        if "start" in command:
            wish_me()
            say_text("Jarvis activated. How can I help you?")
            break
        elif command == "quit":
            say_text("Exiting Jarvis.")
            return
    
    # Main command loop - runs until user says stop
    jarvis_active: bool = True
    while jarvis_active:
        command: str = take_command()
        jarvis_active = process_command(command)

if __name__ == "__main__":
    main()
