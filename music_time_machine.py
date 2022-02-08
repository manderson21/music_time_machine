from bs4 import BeautifulSoup
import requests
import requests_oauthlib
import argparse
import os
import dotenv

# Constants
SELECTOR = "li.lrv-u-flex-grow-1:first-child"
URL = "https://www.billboard.com/charts/hot-100"

dotenv.load_dotenv("./.env")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
SCOPE = ["playlist-modify-public"]

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
oauth = requests_oauthlib.OAuth2Session(client_id=CLIENT_ID,
                                        redirect_uri=REDIRECT_URI,
                                        scope=SCOPE)

auth_url, state = oauth.authorization_url(url="https://accounts.spotify.com/authorize")

auth_response = input(f"Please go to {auth_url} and authorize access.\n"
      f"Enter the full callback URL")

token = oauth.fetch_token(token_url="https://accounts.spotify.com/api/token",
                          authorization_response=auth_response,
                          client_secret=CLIENT_SECRET)

user_data = oauth.get("https://api.spotify.com/v1/me").json()

