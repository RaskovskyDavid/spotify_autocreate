import json

from bs4 import BeautifulSoup
from secret import client_id, client_secret, uri
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import requests

what_year = input("what year you would like to travel to? Type the date in this YYY-MM-DD format: ")

date = what_year.split("-")[0]
path = f"https://www.billboard.com/charts/hot-100/{what_year}"
response = requests.get(url=path)
soup = BeautifulSoup(response.text, "html.parser")
titles = soup.find_all(name="span", class_="chart-element__information__song text--truncate color--primary")
list_titles = [title.getText() for title in titles]
auth_manager = SpotifyClientCredentials(client_id= client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=uri,
                                               scope="playlist-modify-private",
                                               show_dialog=True,
                                               cache_path="token.txt"
                                               ))

user_id = sp.current_user()["id"]
list_urls = []
for song in list_titles:
    result = sp.search(q=f"track:{song}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        list_urls.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=list_urls)


