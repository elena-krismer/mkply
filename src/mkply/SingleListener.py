import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import random

class SingleListener:
    # wrappe for spotipy library
    def __init__(self, client_id, client_secret, redirect_uri):
        self.clientID = client_id
        self.secret = client_secret
        self.redirect_uri = redirect_uri
        self.spotipy_object = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri = redirect_uri,
            scope = "user-top-read" #https://developer.spotify.com/documentation/general/guides/authorization/scopes/
            ))
        self.top_tracks = self.spotipy_object.current_user_top_tracks(limit = 100)
        self.top_artists = self.spotipy_object.current_user_top_artists(limit = 100)

    def save_playlist(self, name = None):
        if name is None:
            name = "random"

        pass

    def playlist_based_on_single_song(self, songID = None, save_playlist = False):
        if songID is None:
            print("")
            song = random.choice(self.top_tracks['items'])
            
        if save_playlist:
            raise NotImplementedError

        pass