import json
import time
import base64
from os import path, getenv

import dotenv
from requests_oauthlib import OAuth2Session


class Authentication(OAuth2Session):
    def __init__(self, cache_path: str, **kwargs):
        super().__init__(**kwargs)
        self.cache_path = cache_path

        dotenv.load_dotenv("../.env")
        self.client_id = getenv("CLIENT_ID")
        self.redirect_uri = getenv("REDIRECT_URI")

    def auth_spotify(self, scope: list[str]):
        self.scope = scope

        authorization_endpoint_url = "https://accounts.spotify.com/authorize"
        token_url = "https://accounts.spotify.com/api/token"

        # Use cached token
        if path.exists(self.cache_path):
            with open(self.cache_path, mode="r") as fin:
                self.token = json.load(fin)

            # Check if token is expired
            if self.token["expires_at"] < time.time():
                encoded_client = base64.b64encode(f"{self.client_id}:{getenv('CLIENT_SECRET')}".encode()).decode()
                headers = {
                    "Authorization": f"Basic {encoded_client}",
                    "Content-Type": "application/x-www-form-urlencoded"
                }
                self.refresh_token(token_url=token_url, headers=headers)
                self.cache_token()

        # Fetch a token
        else:
            auth_url, state = self.authorization_url(url=authorization_endpoint_url)
            auth_response = input(f"Please go to the following link and authorize: {auth_url}\n"
                                  f"Paste the full redirect URL here: ")
            token = self.fetch_token(token_url=token_url,
                                     authorization_response=auth_response,
                                     client_secret=getenv("CLIENT_SECRET"))
            self.cache_token()

    def cache_token(self):
        with open(self.cache_path, mode="w") as fout:
            json.dump(self.token, fout, indent=4)
