# Jarvis - AI Voice Assistant 🤖

A modern Python-based voice assistant powered by OpenAI, OpenWeather API, and Google Speech Recognition. Built with `uv` for fast dependency management.

## ✨ Features

- 🎤 **Voice Commands** - Recognize and execute voice commands using Google Speech Recognition
- 🌤️ **Weather Retrieval** - Get accurate weather information via OpenWeather API with city-specific queries
- 🤖 **AI Responses** - Intelligent responses using OpenAI GPT-3.5 Turbo via OpenRouter
- 🌐 **Web Browsing** - Open websites directly via voice commands (YouTube, Google, GitHub, Stack Overflow, Gmail, Wikipedia)
- 📅 **Date & Time** - Get current date and time with voice commands
- 🔊 **Text-to-Speech** - Audio feedback and responses using pyttsx3
- 💧 **Water Reminder** - Hourly hydration reminders running in background
- 📝 **Type Hints** - 100% Python type annotations for code clarity and IDE support
- ⚠️ **Error Handling** - Robust exception handling with user-friendly messages and graceful fallbacks

## 📦 Installation

### Prerequisites
- **Python 3.13+** (as specified in pyproject.toml)
- Microphone (for voice input)
- Internet connection for API services
- UV package manager (optional but recommended)

### Quick Start

1. **Clone/Download the project:**
```bash
cd d:\Jarvis
```

2. **Install dependencies using uv (recommended):**
```bash
uv sync
```

Or with pip:
```bash
pip install -r requirements.txt
```

3. **Create a `.env` file in the project root with your API keys:**
```env
OPEN_WEATHER_API_KEY=your_openweather_api_key_here
OPEN_ROUTER_API_KEY=your_openrouter_api_key_here
```

### Getting API Keys

**🔑 OpenWeather API:**
- Visit: https://openweathermap.org/api
- Sign up for a free account (provides 1000 calls/day)
- Copy your API key from the account dashboard

**🔑 OpenRouter API:**
- Visit: https://openrouter.ai
- Sign up and create an account
- Get your API key from settings
- Add credits to your account for API usage

## 🚀 Usage

### Running Jarvis

```bash
uv run main.py
```

Or directly with Python:
```bash
python main.py
```

### Starting the Assistant

1. Run the program
2. Say **"start"** to activate Jarvis
3. Jarvis will greet you based on the time of day
4. Issue voice commands (see table below)
5. Say **"stop"** to exit

### Voice Commands

| Command | Example | Description |
|---------|---------|-------------|
| **Start** | "start" | Activate Jarvis after launch |
| **Stop** | "stop" | Exit the application gracefully |
| **Quit** | "quit" | Exit before activation |
| **Weather** | "weather in London" | Get weather for specific city |
| | "weather" | Asks for city name if not provided |
| **Open Website** | "open youtube" | Opens website in default browser |
| | "open google" | Supported: youtube, google, github, stackoverflow, gmail, wikipedia |
| **Date** | "date" | Returns current date (DD-MM-YYYY) |
| **Time** | "time" | Returns current time (HH:MM:SS) |
| **AI Query** | "ai tell me a joke" | Get AI response from GPT-3.5 Turbo |
| | "ai what is python" | AI processes any text-based query |

## 📁 Project Structure

```
d:\Jarvis\
├── main.py                   # Main application with all functions
├── pyproject.toml            # Project metadata & dependencies (uv managed)
├── requirements.txt          # Pip-compatible dependency list
├── .env                      # API keys configuration (create this)
├── .gitignore                # Git ignore patterns
└── README.md                 # Project documentation
```

### Directory Overview
- **main.py**: Core application containing all voice assistant functions
  - ~224 lines of well-documented Python code
  - Full type hints throughout
  - Comprehensive error handling

## 🔧 Code Architecture

### Main Functions

#### `take_command() -> str`
Listens to microphone input and converts speech to text.
- Uses Google Speech Recognition API
- Automatically adjusts for ambient noise
- Pause threshold: 1 second
- Returns empty string if audio can't be understood
- Error handling for network and audio issues

#### `process_command(command: str) -> bool`
Processes voice commands and executes corresponding actions.
- Returns True to continue, False to stop execution
- Handles: open website, date, time, weather, AI queries
- Falls back with user-friendly messages for unknown commands

#### `get_weather(city_name: str) -> str`
Fetches real-time weather data from OpenWeather API.
- Returns: temperature (°C), description, humidity (%), wind speed (m/s)
- Handles network timeouts and API errors gracefully
- Provides specific error messages (e.g., "City not found")
- **Parameters**: city_name (string)
- **Returns**: Weather info string or error message

#### `get_ai_response(user_query: str) -> Optional[str]`
Gets AI-powered responses using OpenRouter API with GPT-3.5 Turbo.
- Maximum 50 tokens per response (concise answers)
- Temperature: 0.5 (balanced creativity)
- Graceful error handling with fallback message
- **Parameters**: user_query (string)
- **Returns**: AI response string or None on error

#### `open_website(site_name: str) -> None`
Opens websites from the predefined Site dictionary.
- **Supported websites**: youtube, google, github, stackoverflow, gmail, wikipedia
- Announces action via text-to-speech
- Error handling for unsupported website names

#### `say_text(text: str) -> None`
Converts text to speech and plays audio output using pyttsx3.
- Non-blocking text-to-speech
- Exception handling to prevent crashes
- Used for all user feedback

#### `wish_me() -> None`
Greets user based on current time of day.
- **Morning** (00:00-11:59): "Good Morning!"
- **Afternoon** (12:00-17:59): "Good Afternoon!"
- **Evening** (18:00-23:59): "Good Evening!"

#### `water_reminder() -> None`
Runs in a background daemon thread.
- Reminds user to drink water every hour (3600 seconds)
- Executes continuously without blocking main application

## 📦 Dependencies

Managed via `pyproject.toml` and installed with `uv sync`.

| Package | Version | Purpose |
|---------|---------|---------|
| **pyttsx3** | >=2.99 | Text-to-speech synthesis |
| **SpeechRecognition** | >=3.14.5 | Speech-to-text recognition |
| **python-dotenv** | >=1.2.1 | Environment variable management |
| **requests** | >=2.31.0 | HTTP requests for APIs |
| **openai** | >=2.15.0 | OpenAI API client |
| **pyaudio** | >=0.2.14 | Audio input/output device handling |
| **wikipedia** | >=1.4.0 | Wikipedia queries (optional enhancement) |

### Installation Methods

**Using uv (recommended - faster):**
```bash
uv sync
```

**Using pip:**
```bash
pip install -r requirements.txt
```

**Install individual package:**
```bash
uv pip install pyttsx3
```

## ⚙️ Configuration

### Site Dictionary
Add or modify supported websites in the `Site` dictionary at the top of `main.py`:
```python
Site: Dict[str, str] = {
    "youtube": 'https://www.youtube.com/',
    "google": 'https://www.google.com/', 
    "github": 'https://www.github.com/ShaikhHamza104',
    "stackoverflow": 'https://stackoverflow.com/',
    "gmail": 'https://mail.google.com/',
    "wikipedia": 'https://www.wikipedia.org/'
    # Add more sites here as needed
}
```

### Audio Configuration
Adjust microphone settings in the `take_command()` function:
```python
recognizer.pause_threshold = 1  # Silence duration to end phrase (seconds)
recognizer.adjust_for_ambient_noise(source, duration=0.5)  # Noise calibration
```

### AI Model Settings
Customize AI responses in `get_ai_response()`:
```python
response = client.chat.completions.create(
    model="openai/gpt-3.5-turbo",  # Change model if desired
    max_tokens=50,  # Adjust response length
    temperature=0.5,  # 0.0 (deterministic) to 1.0 (creative)
)
```

## 🔍 Troubleshooting

### Microphone Issues
- **Symptom**: "Microphone not found" or audio errors
- **Solutions**:
  - Verify microphone is connected and enabled in system settings
  - Test audio device: `python -m pyaudio`
  - Update audio drivers
  - Check for conflicting applications using audio

### Weather API Problems
- **Symptom**: Returns "City not found" or wrong temperature
- **Solutions**:
  - Verify `OPEN_WEATHER_API_KEY` is correct in `.env`
  - Check internet connection
  - OpenWeather free tier: 1000 calls/day limit
  - Ensure city name spelling is correct

### AI Response Not Working
- **Symptom**: "I'm having trouble right now" message
- **Solutions**:
  - Verify `OPEN_ROUTER_API_KEY` is valid in `.env`
  - Check OpenRouter account has sufficient credits
  - Verify internet connection is stable
  - Check API key permissions in OpenRouter dashboard

### Speech Recognition Fails
- **Symptom**: "I could not understand the audio"
- **Solutions**:
  - Reduce background noise in environment
  - Speak clearly and at normal pace
  - Increase `pause_threshold` in code if speech is choppy
  - Adjust microphone input level in system settings
  - Check Google Speech Recognition API availability

### No Sound Output
- **Symptom**: Program runs but no audio feedback
- **Solutions**:
  - Check system volume and speaker settings
  - Test: `python -c "import pyttsx3; pyttsx3.init().say('test'); pyttsx3.init().runAndWait()"`
  - Verify speakers/headphones are connected
  - Check for pyttsx3 engine errors in console output

## 👨‍💻 Development

### Code Quality Standards
- ✅ **100% Type Hints**: All functions fully annotated
- ✅ **PEP 8 Compliant**: Follows Python style guidelines
- ✅ **Error Handling**: Comprehensive try-except blocks
- ✅ **Documentation**: Docstrings for all functions
- ✅ **Clean Code**: Well-organized and readable

### Syntax Validation
```bash
# Check Python syntax
python -m py_compile main.py

# Validate AST
python -c "import ast; ast.parse(open('main.py').read())"

# Run with debugging
python -u main.py
```

### Code Metrics
- **Lines of code**: ~224 (main.py)
- **Number of functions**: 8
- **Type hint coverage**: 100%
- **Docstring coverage**: 100%

### Type Hints Example
```python
from typing import Dict, Optional

def get_weather(city_name: str) -> str:
    """Fetch weather information for a city using OpenWeather API."""
    
def get_ai_response(user_query: str) -> Optional[str]:
    """Get AI response using OpenRouter API with GPT-3.5 Turbo model."""
    
Site: Dict[str, str] = {...}
```

## 🚀 Future Enhancements

- [ ] Add local speech recognition (offline support)
- [ ] Integrate multiple AI models beyond GPT-3.5
- [ ] Calendar integration for scheduling
- [ ] Multi-language support
- [ ] Persistent conversation history
- [ ] Custom wake word detection ("Jarvis")
- [ ] Note-taking functionality
- [ ] Email sending via voice
- [ ] News briefing feature
- [ ] Music playback integration
- [ ] Smart home integration (IoT devices)
- [ ] User profile customization

## 📋 Performance Notes

- **Startup time**: ~1-2 seconds
- **Voice recognition latency**: 1-3 seconds
- **API response time**: 1-2 seconds (depends on network)
- **Memory usage**: ~50-100 MB while running
- **Background thread**: Water reminder runs with minimal overhead

## 🔐 Security Considerations

- Never commit `.env` file to version control
- Keep API keys private and regenerate if exposed
- Use environment variables for sensitive data
- Consider rate limiting for public deployments
- Validate user input before sending to APIs

## 📝 License & Attribution

This project is open source and available for personal use.

**Author**: Shaikh Hamza  
**Created**: January 2026  
**Python Version Required**: 3.13+  
**Package Manager**: UV (uv.io)

---

## 🆘 Support & Contribution

For issues, improvements, or feature requests:
1. Check the Troubleshooting section
2. Review error messages in console output
3. Verify API keys are correctly configured
4. Check internet connection stability

**Made with ❤️ using Python 3.13+**
