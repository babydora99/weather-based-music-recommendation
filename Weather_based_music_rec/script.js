const locationInput = document.getElementById('location');
const getMusicButton = document.getElementById('get-music');
const musicRecommendationsDiv = document.getElementById('music-recommendations');
const songsGrid = document.getElementById('songs-grid');
const loadingDiv = document.getElementById('loading');
const weatherInfoDiv = document.getElementById('weather-info');
const errorMessageDiv = document.getElementById('error-message');

const api_key = '78e879102c7d7274e73c737727f975de';

// Weather icon mapping
const weatherIcons = {
    'Clear': '☀️',
    'Clouds': '☁️',
    'Rain': '🌧️',
    'Drizzle': '🌦️',
    'Thunderstorm': '⛈️',
    'Snow': '❄️',
    'Mist': '🌫️',
    'Fog': '🌫️',
    'Haze': '🌫️'
};

getMusicButton.addEventListener('click', async () => {
    const location = locationInput.value.trim();
    if (!location) {
        showError('Please enter a location');
        return;
    }

    // Reset UI
    hideError();
    hideWeatherInfo();
    hideMusicRecommendations();
    showLoading();

    try {
        const weatherData = await getWeatherData(location);
        if (!weatherData || weatherData.cod !== 200) {
            hideLoading();
            showError('Location not found or error fetching weather data');
            return;
        }

        displayWeatherInfo(weatherData);
        const musicRecommendations = await getMusicRecommendations(weatherData);
        hideLoading();
        displayMusicRecommendations(musicRecommendations);
    } catch (error) {
        hideLoading();
        console.error('Error:', error);
        showError('Something went wrong. Please try again later.');
    }
});

async function getWeatherData(location) {
    const response = await fetch(`https://api.openweathermap.org/data/2.5/weather?q=${encodeURIComponent(location)}&appid=${api_key}&units=metric`);
    if (!response.ok) {
        throw new Error(`Weather API error: ${response.statusText}`);
    }
    const data = await response.json();
    return data;
}

async function getMusicRecommendations(weatherData) {
    const response = await fetch('/music-recommendations', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(weatherData),
    });
    if (!response.ok) {
        throw new Error(`Music API error: ${response.statusText}`);
    }
    const data = await response.json();
    return data;
}

function displayWeatherInfo(weatherData) {
    const cityName = document.getElementById('city-name');
    const weatherCondition = document.getElementById('weather-condition');
    const temperature = document.getElementById('temperature');
    const weatherIcon = document.getElementById('weather-icon');

    const condition = weatherData.weather[0].main;
    const temp = Math.round(weatherData.main.temp);

    cityName.textContent = weatherData.name;
    weatherCondition.textContent = condition;
    temperature.textContent = `${temp}°C`;
    weatherIcon.textContent = weatherIcons[condition] || '🌡️';

    showWeatherInfo();
}

function displayMusicRecommendations(musicRecommendations) {
    songsGrid.innerHTML = '';
    if (!Array.isArray(musicRecommendations) || musicRecommendations.length === 0) {
        songsGrid.innerHTML = '<p class="no-results">No music recommendations found.</p>';
        showMusicRecommendations();
        return;
    }

    musicRecommendations.forEach((recommendation) => {
        const musicElement = document.createElement('div');
        musicElement.className = 'song-card';
        musicElement.innerHTML = `
            <div class="song-poster">
                <img src="${recommendation.poster}" alt="${recommendation.song}" onerror="this.src='https://i.postimg.cc/0QNxYz4V/social.png'">
            </div>
            <div class="song-info">
                <p class="song-name">${recommendation.song}</p>
            </div>
        `;
        songsGrid.appendChild(musicElement);
    });

    showMusicRecommendations();
}

// UI Helper functions
function showLoading() {
    loadingDiv.classList.remove('hidden');
}

function hideLoading() {
    loadingDiv.classList.add('hidden');
}

function showWeatherInfo() {
    weatherInfoDiv.classList.remove('hidden');
}

function hideWeatherInfo() {
    weatherInfoDiv.classList.add('hidden');
}

function showMusicRecommendations() {
    musicRecommendationsDiv.classList.remove('hidden');
}

function hideMusicRecommendations() {
    musicRecommendationsDiv.classList.add('hidden');
}

function showError(message) {
    errorMessageDiv.textContent = message;
    errorMessageDiv.classList.remove('hidden');
}

function hideError() {
    errorMessageDiv.classList.add('hidden');
}
