from bs4 import BeautifulSoup
import requests
import sys


class TopSongs:
    def __init__(self, url: str, song_selector: str, artist_selector: str):
        self.songs = None
        self.url = url
        self.song_selector = song_selector
        self.artist_selector = artist_selector

    def get_songs(self, date: str, parser: str):
        try:
            response = requests.get(f"{self.url}/{date}")
            response.raise_for_status()
        except requests.HTTPError as e:
            print(f"Incorrect Date: {e}")
            sys.exit(1)

        soup = BeautifulSoup(response.text, features=parser)
        song_tags = soup.select(self.song_selector)
        artist_tags = soup.select(self.artist_selector)

        self.songs = [
            {
                "song": song_tags[i].getText().strip(),
                "artist": artist_tags[i].getText().strip()
            }
            for i in range(len(song_tags))
        ]
