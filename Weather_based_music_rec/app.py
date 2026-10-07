# import requests

# api_key='78e879102c7d7274e73c737727f975de'
# user_input=input("Enter your Location:")
# weather_data=requests.get(
#     f"http://api.openweathermap.org/data/2.5/weather?q={user_input}&appid={api_key}&units=metric")

# #SPOTIFY_CLIENT_ID = "b03d347d77da410b8f7a5df890eb7221"
# #SPOTIFY_CLIENT_SECRET = "1c38c054c3ef48d6b2f3428a38291481"


# if weather_data.json()['code']==404:
#     print("No City found")
# else:
#     weather=weather_data.json()['weather'][0]['main']
# temp=round(weather_data.json()['main']['temp'])

# print(f"The weather in {user_input} is : {weather}")
# print(f"The temp in {user_input} is : {temp}°F")


import pickle
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from flask import Flask, request, jsonify, send_from_directory
#import os
app = Flask(__name__)

@app.route('/')
def home():
    return send_from_directory(app.root_path, 'index.html')

@app.route('/style.css')
def stylesheet():
    return send_from_directory(app.root_path, 'style.css')

@app.route('/script.js')
def frontend_script():
    return send_from_directory(app.root_path, 'script.js')

CLIENT_ID = "b03d347d77da410b8f7a5df890eb7221"
CLIENT_SECRET = "1c38c054c3ef48d6b2f3428a38291481"


# Initialize the Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_song_album_cover_url(song_name, artist_name):
    try:
        search_query = f"track:{song_name} artist:{artist_name}"
        results = sp.search(q=search_query, type="track")
        if results and results["tracks"]["items"]:
            track = results["tracks"]["items"][0]
            album_cover_url = track["album"]["images"][0]["url"]
            return album_cover_url
        else:
            return "https://i.postimg.cc/0QNxYz4V/social.png"
    except Exception as e:
        print(f"Spotify API error: {e}")
        return "https://i.postimg.cc/0QNxYz4V/social.png"

def recommend(song):
    try:
        with open('df.pkl', 'rb') as df_file:
            music = pickle.load(df_file)
        with open('similarity.pkl', 'rb') as sim_file:
            similarity = pickle.load(sim_file)
    except FileNotFoundError as e:
        return ["Error: File not found."], ["https://i.postimg.cc/0QNxYz4V/social.png"]
    except Exception as e:
        return [f"Error: {str(e)}"], ["https://i.postimg.cc/0QNxYz4V/social.png"]

    try:
        index = music[music['song'] == song].index[0]
    except IndexError:
        return ["Song not found in database."], ["https://i.postimg.cc/0QNxYz4V/social.png"]

    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_music_names = []
    recommended_music_posters = []
    for i in distances[1:6]:
        artist = music.iloc[i[0]].artist
        recommended_music_posters.append(get_song_album_cover_url(music.iloc[i[0]].song, artist))
        recommended_music_names.append(music.iloc[i[0]].song)
    return recommended_music_names, recommended_music_posters

def get_song_for_weather(condition):
    song_map = {
        'Clear': 'Happy',
        'Rain': 'Someone Like You',
        'Clouds': 'Let Her Go',
        'Snow': 'Let It Go',
        'Thunderstorm': 'Radioactive',
        'Drizzle': 'Photograph',
        'Mist': 'Stay'
    }
    return song_map.get(condition, 'Shape of You')

@app.route('/music-recommendations', methods=['POST'])
def get_music_recommendations():
    try:
        weather_data = request.get_json()
        if not weather_data or 'weather' not in weather_data:
            return jsonify([{"song": "Error: Invalid weather data", "poster": "https://i.postimg.cc/0QNxYz4V/social.png"}]), 400

        weather_condition = weather_data['weather'][0]['main']
        song = get_song_for_weather(weather_condition)
        names, posters = recommend(song)
        result = [{"song": name, "poster": poster} for name, poster in zip(names, posters)]
        return jsonify(result)
    except Exception as e:
        print(f"Error in get_music_recommendations: {e}")
        return jsonify([{"song": f"Error: {str(e)}", "poster": "https://i.postimg.cc/0QNxYz4V/social.png"}]), 500

if __name__ == '__main__':
    app.run(debug=True)
