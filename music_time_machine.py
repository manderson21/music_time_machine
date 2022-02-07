from bs4 import BeautifulSoup
import requests
import argparse

SELECTOR = "li.lrv-u-flex-grow-1:first-child"
URL = "https://www.billboard.com/charts/hot-100"

parser = argparse.ArgumentParser(description="Create a playlist of the Billboard Hot 100 from any given date")
parser.add_argument("date", type=str, help="YYYY-MM-DD - Date to pick music from")

args = parser.parse_args()
date = args.date

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


