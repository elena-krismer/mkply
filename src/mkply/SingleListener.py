import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import random
from collections import Counter
import randomname


class SingleListener:
    # wrappe for spotipy library
    def __init__(self, client_id, client_secret, redirect_uri, user_id = None, limit = 100):
        """Object includes two Spotipy objects: 
        1. to access top artists/tracks of the listener
        2. to create playlist and save them in your spotify account

        Args:
            client_id (_type_): client_id https://developer.spotify.com/documentation/general/guides/authorization/app-settings/
            client_secret (_type_): client_secret https://developer.spotify.com/documentation/general/guides/authorization/app-settings/
            redirect_uri (_type_): the same uri you have specified in your setttings
            user_id (_type_, optional): not the same as your client_id. go to your spotify profile -> account
            is required in order to create a playlist
            limit (int, optional): Limit of top songs/artist. Defaults to 100.
        """
        self.clientID = client_id
        self.secret = client_secret
        self.redirect_uri = redirect_uri
        self.spotipy_object = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri = redirect_uri,
            scope = "user-top-read" #https://developer.spotify.com/documentation/general/guides/authorization/scopes/
            ))
        self.spotipy_object_playlist_creation = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri = redirect_uri,
            scope = "playlist-modify-public" #https://developer.spotify.com/documentation/general/guides/authorization/scopes/
            ))
        self.user_id = user_id
        self.top_tracks = self.spotipy_object.current_user_top_tracks(limit = limit)
        self.top_artists = self.spotipy_object.current_user_top_artists(limit = limit)
        self.artist_ranking = self.rank_artists()


    def save_playlist(self, tracks_list, name = None):
        """save playlist in your spotify profile
        user_id most be specified in object

        Args:
            tracks_list (list): _description_
            name (string, optional): name of playlist, else (very) random name will be created. Defaults to None.

        Raises:
            ValueError: if user_id is none
        """
        if self.user_id is None:
            raise ValueError("user_id must be specified in object in order to create a playlist")
        if name is None:
            name = randomname.get_name()
        playlist = self.spotipy_object_playlist_creation.user_playlist_create(user =self.user_id, name =name, public=True, collaborative=False, description='')
        self.spotipy_object_playlist_creation.playlist_add_items(playlist_id = playlist.get("id"), items = tracks_list, position=None)
        print("Playlist: " + name + " has been saved")
        print("Playlist can be found here: ", playlist.get("external_urls").get("spotify"))

    
    def rank_artists(self):
        """Creates a dict with the ranking of the artists. and related artist (more suitable for multiple listeners)

        Returns:
            _type_: Counter dict with artist_id as key and value is the count/ranking of the artist
        """
        ranked_artists_dict = Counter()
        # get top artist for each Listener object
       
        for item in self.top_artists["items"]:
            # get the artist id
            artist_id = item.get("id")
            if artist_id in ranked_artists_dict:
                ranked_artists_dict[artist_id] =  ranked_artists_dict.get(artist_id) + 2
            else: 
                ranked_artists_dict[artist_id] =  2  
            # get related artists increase by 1
            for related_artist in self.spotipy_object.artist_related_artists(artist_id)["artists"]:
                related_artist_id = related_artist.get("id")
                if related_artist_id in ranked_artists_dict:
                    ranked_artists_dict[related_artist_id] =  ranked_artists_dict.get(related_artist_id) + 1
                else:
                    ranked_artists_dict[related_artist_id] =  1   
        return ranked_artists_dict


    def create_playlist(self, n_songs = 25, genre = None, n_artists = 25, save = False, name = None):
        """creates a random playlist based in your top artists (atm)

        Args:
            n_songs (int, optional): number of songs in the playlist. Defaults to 25.
            genre (_type_, optional): _description_. Defaults to None.
            n_artists (int, optional): number of top artists chosen. Defaults to 25.
            save (bool, optional): whether playlist should be saved in account. 
            user_id must be specified in the object. Defaults to False.
            name (_type_, optional): name of playlist. if not specified (very) random 
            name is created. Defaults to None.

        Raises:
            NotImplementedError: _description_

        Returns:
            _type_: _description_
        """
        # unnested Counter output with artist ids
        artist_list = [item[0] for item in self.artist_ranking.most_common(n_artists)]
        song_list = []

        if genre is not None:
            raise NotImplementedError("Creating a Playlist based on a genre has not been implemented yet")

        for artist in artist_list:
            tracks = self.spotipy_object.artist_top_tracks(artist_id = artist)
            for track in tracks["tracks"]:
                song_list.append(track.get("id"))
        
        if len(song_list) < n_songs:
            n_songs = len(song_list)
            print("n_songs is to high, playlist will have " + n_songs + " songs")
        
        tracks_list = random.choices(song_list, k=n_songs)
        if save == True:
            self.save_playlist(tracks_list = tracks_list, name = name)
        else:
            return tracks_list


    def playlist_based_on_single_song(self, songID = None, save_playlist = False):
        if songID is None:
            song = random.choice(self.top_tracks['items'])
            print("No song selected, choose random song: ", song.get("name"))
            songID = song.get("id")
            
        if save_playlist:
            raise NotImplementedError

        pass