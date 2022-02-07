from bs4 import BeautifulSoup
import requests
import argparse

parser = argparse.ArgumentParser(description="Create a playlist of the Billboard Hot 100 from any given date")
parser.add_argument("date", type=str, help="YYYY-MM-DD - Date to pick music from")

args = parser.parse_args()
date = args.date

url = f"https://www.billboard.com/charts/hot-100/{date}"

response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.text, features="html.parser")


