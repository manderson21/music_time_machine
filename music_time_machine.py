from bs4 import BeautifulSoup
import requests
import argparse
import spotipy
import os
import dotenv

# Constants
SELECTOR = "li.lrv-u-flex-grow-1:first-child"
URL = "https://www.billboard.com/charts/hot-100"

dotenv.load_dotenv("./.env")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# Argument Parsing
parser = argparse.ArgumentParser(description="Create a playlist of the Billboard Hot 100 from any given date")
parser.add_argument("date", type=str, help="YYYY-MM-DD - Date to pick music from")

args = parser.parse_args()
date = args.date

# Web Scraping the top 100 songs
response = requests.get(f"{URL}/{date}")
response.raise_for_status()

soup = BeautifulSoup(response.text, features="html.parser")

top_songs = [
    {
        "Song": tag.select_one("h3").getText().strip(),
        "Artist": tag.select_one("span").getText().strip()
    }
    for tag in soup.select(SELECTOR)
]

# Authenticating with spotify
sp = spotipy.Spotify(auth_manager=spotipy.SpotifyOAuth(client_id=CLIENT_ID,
                                                       client_secret=CLIENT_SECRET,
                                                       redirect_uri="https://example.com",
                                                       scope="playlist-modify-public"))
user_data = sp.current_user()



