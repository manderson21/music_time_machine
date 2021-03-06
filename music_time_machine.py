import argparse
import os
import dotenv

import topsongs
import authentication

# Constants
SELECTOR = "li.lrv-u-flex-grow-1:first-child"
URL = "https://www.billboard.com/charts/hot-100"
API_URL = "https://api.spotify.com/v1"

dotenv.load_dotenv("./.env")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
SCOPE = ["playlist-modify-public", "playlist-modify-private"]

# Argument Parsing
arg_parser = argparse.ArgumentParser(description="Create a playlist of the Billboard Hot 100 from any given date")
arg_parser.add_argument("date", type=str, help="YYYY-MM-DD - Date to pick music from")
arg_parser.add_argument("is_public", type=bool, help="True - To create a public playlist\n"
                                                     "False - To create a private playlist")

args = arg_parser.parse_args()
date = args.date
is_public = args.is_public

# Web Scraping the top 100 songs
top_songs = topsongs.TopSongs(URL, song_selector=f"{SELECTOR} h3", artist_selector=f"{SELECTOR} span")
top_songs.get_songs(date, parser="html.parser")

# Authentication
api = authentication.Authentication(".cache")
api.auth_spotify(scope=SCOPE)

# Get songs

song_ids = []
for song in top_songs.songs:
    params = {
        "type": "track",
        "q": f"track:{song['song']}, artist:{song['artist']}"
    }
    response = api.get(f"{API_URL}/search", params=params)
    json = response.json()
    items = json["tracks"]["items"]
    if items:
        song_ids.append(items[0]["uri"])

# Create playlist
user = api.get(f"{API_URL}/me").json()
json = {
    "name": f"Top 100 songs of {date}",
    "public": is_public,
    "description": f"Top 100 songs of {date}"
}
response = api.post(f"{API_URL}/users/{user['id']}/playlists", json=json).json()
playlist_id = response["id"]

# Add songs to playlist
json = {
    "uris": song_ids
}
response = api.post(f"{API_URL}/playlists/{playlist_id}/tracks", json=json)
