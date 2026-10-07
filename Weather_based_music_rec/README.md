# Weather Based Music Recommendation

A modern web application that recommends songs based on the current weather in a user-provided location. The backend fetches live weather data from OpenWeatherMap, maps the weather condition to a seed song, and then uses a precomputed similarity model to suggest related tracks.

## Project Overview

This project combines weather data with music recommendations to create a mood-based music discovery experience. When you enter a city name, the app:
1. Fetches current weather conditions (temperature, weather type)
2. Maps the weather condition to a mood-appropriate seed song
3. Uses a similarity model to find 5 similar songs
4. Displays the recommendations in a beautiful, responsive UI

## Features

- 🌍 **City-based Weather Search**: Enter any city name to get current weather data
- 🌡️ **Weather Display**: Shows city name, weather condition, temperature, and weather icon
- 🎵 **Smart Music Recommendations**: Recommends 5 songs based on weather mood
- 🎨 **Modern UI**: Beautiful gradient design with responsive layout
- ⚡ **Real-time API Integration**: Live weather data from OpenWeatherMap
- 🎯 **Weather-based Moods**: Different songs for Clear, Rain, Clouds, Snow, Thunderstorm, Drizzle, and Mist
- 📱 **Mobile Responsive**: Works seamlessly on desktop and mobile devices
- ⚠️ **Error Handling**: Graceful error handling with user-friendly messages
- 🔄 **Loading States**: Visual feedback during API calls

## Tech Stack

### Backend
- **Python 3.13**: Core programming language
- **Flask**: Web framework for the backend API
- **Spotipy**: Spotify API wrapper for album art (optional)
- **Pandas**: Data manipulation for song dataset
- **NumPy**: Numerical operations for similarity calculations
- **Pickle**: Model serialization for dataset and similarity matrix

### Frontend
- **HTML5**: Structure and layout
- **CSS3**: Modern styling with gradients, animations, and responsive design
- **JavaScript (ES6+):** API calls, DOM manipulation, and state management

### APIs
- **OpenWeatherMap API**: Weather data and forecasts
- **Spotify API**: Album art fetching (requires valid credentials)

## Project Structure

```
Weather_based_music_rec/
├── .venv/                    # Virtual environment (Python packages)
├── app.py                    # Flask backend with recommendation logic
├── index.html                # Frontend UI structure
├── script.js                 # Frontend JavaScript for API calls
├── style.css                 # Modern styling and responsive design
├── df.pkl                    # Song dataset (Pandas DataFrame)
├── similarity.pkl            # Precomputed similarity matrix
├── spotify_millsongdata.csv  # Source dataset for training
├── Model_training.ipynb      # Jupyter notebook for model training
└── README.md                 # Project documentation
```

## Input and Output

### Input
- **User Input**: City name (e.g., "London", "New York", "Tokyo")
- **Weather Data**: Fetched from OpenWeatherMap API containing:
  - City name
  - Weather condition (Clear, Rain, Clouds, Snow, Thunderstorm, Drizzle, Mist)
  - Temperature in Celsius

### Output
- **Weather Information**:
  - City name
  - Weather condition with emoji icon
  - Temperature in Celsius
- **Music Recommendations**: 5 songs with:
  - Song name
  - Album art (placeholder image if Spotify API is unavailable)

### Weather to Song Mapping
| Weather Condition | Seed Song | Mood |
|-------------------|------------|------|
| Clear | Happy | Cheerful, upbeat |
| Rain | Someone Like You | Melancholic, emotional |
| Clouds | Let Her Go | Reflective, calm |
| Snow | Let It Go | Magical, peaceful |
| Thunderstorm | Radioactive | Intense, energetic |
| Drizzle | Photograph | Nostalgic, gentle |
| Mist | Stay | Atmospheric, relaxed |
| Default | Shape of You | Popular, versatile |

## Prerequisites

- **Python 3.8+** (tested with Python 3.13)
- **OpenWeatherMap API Key**: Get free at https://openweathermap.org/api
- **Virtual Environment**: Recommended for dependency isolation
- **Required Python Packages**:
  ```bash
  pip install flask spotipy requests pandas numpy
  ```

## Setup Instructions

1. **Clone or download the project**

2. **Navigate to the project directory**:
   ```bash
   cd Weather_based_music_rec
   ```

3. **Create and activate virtual environment** (if not already created):
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On Unix/MacOS:
   source .venv/bin/activate
   ```

4. **Install required packages**:
   ```bash
   pip install flask spotipy requests pandas numpy
   ```

5. **Update API credentials**:
   - Update `api_key` in `script.js` with your OpenWeatherMap API key
   - Optionally update `CLIENT_ID` and `CLIENT_SECRET` in `app.py` with Spotify credentials for album art (optional - the app works with placeholder images)

6. **Verify required files**:
   Ensure these files are present in the project root:
   - `df.pkl` (song dataset)
   - `similarity.pkl` (similarity matrix)

## Running the Application

1. **Start the Flask server**:
   ```bash
   python app.py
   ```

2. **Open in browser**:
   Navigate to `http://127.0.0.1:5000`

3. **Use the app**:
   - Enter a city name in the search box
   - Click "Get Music" button
   - View weather information and music recommendations

## API Endpoints

### POST /music-recommendations

**Description**: Get music recommendations based on weather data

**Request Body**: Weather JSON data from OpenWeatherMap
```json
{
  "weather": [
    {
      "main": "Clear"
    }
  ],
  "main": {
    "temp": 25
  }
}
```

**Response**: Array of 5 recommended songs
```json
[
  {
    "song": "Gives You Hell",
    "poster": "https://i.postimg.cc/0QNxYz4V/social.png"
  },
  {
    "song": "Happy? - Intwine",
    "poster": "https://i.postimg.cc/0QNxYz4V/social.png"
  }
]
```

## Known Limitations

- **Spotify Album Art**: The current Spotify API credentials don't have an active premium subscription, so album art falls back to a placeholder image. To get actual album art:
  1. Create a Spotify Developer account at https://developer.spotify.com/dashboard
  2. Create a new app to get valid `CLIENT_ID` and `CLIENT_SECRET`
  3. Update the credentials in `app.py`

- **Weather Mapping**: Uses a fixed mapping of weather conditions to seed songs. This could be enhanced with:
  - More sophisticated mood detection
  - User preference learning
  - Time-of-day considerations

- **Dataset**: Based on a static song dataset (`df.pkl`). New songs cannot be added without retraining the model.

## Future Enhancements

- [ ] Add user authentication and personalized recommendations
- [ ] Implement more advanced recommendation algorithms (collaborative filtering, content-based)
- [ ] Add Spotify integration for direct music playback
- [ ] Support for multiple weather API providers
- [ ] Add genre filtering options
- [ ] Implement caching for better performance
- [ ] Add unit tests and integration tests
- [ ] Deploy to cloud platform (Heroku, AWS, etc.)
- [ ] Add dark mode toggle
- [ ] Support for historical weather data

## Error Handling

The app includes comprehensive error handling:
- Invalid city names: Shows error message in UI
- API failures: Graceful fallback with user notification
- Missing data files: Displays appropriate error messages
- Network issues: Retry logic with user feedback

## Security Notes

- API keys are currently hardcoded in the source files
- For production deployment, move sensitive credentials to environment variables:
  ```python
  import os
  CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
  CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
  ```

## License

This project is for educational and personal use.

## Credits

- Weather data powered by [OpenWeatherMap](https://openweathermap.org/)
- Music dataset from [Spotify](https://spotify.com/)
- Built with Flask, Spotipy, and modern web technologies
