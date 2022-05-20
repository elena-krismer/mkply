import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import random

class Listener():
    def __init__(self, client_id, client_secret, redirect_uri, limit = 100):
        self.clientID = client_id
        self.secret = client_secret
        self.redirect_uri = redirect_uri
        self.spotipy_object = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri = redirect_uri,
            scope = "user-top-read" #https://developer.spotify.com/documentation/general/guides/authorization/scopes/
            ))
        self.top_tracks = self.spotipy_object.current_user_top_tracks(limit = limit)
        self.top_artists = self.spotipy_object.current_user_top_artists(limit = limit)


    # save Listener as pickle object
    def save():
        pass

    # should allow to load pickled Listener into object
    @classmethod
    def load():
        x = cls()
        pass