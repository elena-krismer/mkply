#from tkinter import E
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import random
from collections import Counter
import randomname
import json
import collections

# NOTES
# This Should actually be the parent class of the MultiListener object
# OR create extra parent class for Single/MultiListener
# find better way to deal with scopes


class Listener:
    # wrappe for spotipy library
    def __init__(self,
                 client_id,
                 client_secret,
                 redirect_uri,
                 user_id=None,
                 limit=100):
        """Object includes two Spotipy objects: 
        1. to access top artists/tracks of the listener
        2. to create playlist and save them in your spotify account (if user_id provided)

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
            redirect_uri=redirect_uri,
            scope=
            "user-top-read"  #https://developer.spotify.com/documentation/general/guides/authorization/scopes/
        ))
        self.spotipy_object_playlist_creation = None
        if user_id is not None:
            self.spotipy_object_playlist_creation = spotipy.Spotify(
                auth_manager=SpotifyOAuth(
                    client_id=client_id,
                    client_secret=client_secret,
                    redirect_uri=redirect_uri,
                    scope=
                    "playlist-modify-public"  #https://developer.spotify.com/documentation/general/guides/authorization/scopes/
                ))
        self.user_id = user_id
        self.top_tracks = self.spotipy_object.current_user_top_tracks(
            limit=limit)
        self.top_artists = self.spotipy_object.current_user_top_artists(
            limit=limit)
        self.artist_ranking = None
        self.genre_dict = None

    def update_top_tracks_artists(self, limit=100):
        """updates top artists and top tracks of Listener

        Args:
            limit (int, optional): number of top artists/tracks. Defaults to 100.
        """
        old = self.top_tracks
        self.top_tracks = self.spotipy_object.current_user_top_tracks(
            limit=limit)
        self.top_artists = self.spotipy_object.current_user_top_artists(
            limit=limit)
        if old == self.top_tracks:
            print("Everything up to date")
        else:
            print("Favourite artists and tracks have been updated")

    def save_playlist(self, tracks_list, name=None):
        """save playlist in your spotify profile
        user_id most be specified in object

        Args:
            tracks_list (list): _description_
            name (string, optional): name of playlist, else (very) random name will be created. Defaults to None.

        Raises:
            ValueError: if user_id is none
        """
        if self.user_id is None:
            raise ValueError(
                "user_id must be specified in object in order to create a playlist"
            )
        if name is None:
            name = randomname.get_name()
        playlist = self.spotipy_object_playlist_creation.user_playlist_create(
            user=self.user_id,
            name=name,
            public=True,
            collaborative=False,
            description='')
        self.spotipy_object_playlist_creation.playlist_add_items(
            playlist_id=playlist.get("id"), items=tracks_list, position=None)
        print("Playlist: " + name + " has been saved")
        print("Playlist can be found here: ",
              playlist.get("external_urls").get("spotify"))

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
                ranked_artists_dict[artist_id] = ranked_artists_dict.get(
                    artist_id) + 2
            else:
                ranked_artists_dict[artist_id] = 2
            # get related artists increase by 1
            for related_artist in self.spotipy_object.artist_related_artists(
                    artist_id)["artists"]:
                related_artist_id = related_artist.get("id")
                if related_artist_id in ranked_artists_dict:
                    ranked_artists_dict[
                        related_artist_id] = ranked_artists_dict.get(
                            related_artist_id) + 1
                else:
                    ranked_artists_dict[related_artist_id] = 1
        return ranked_artists_dict

    def create_genre_dict(self):
        """create dict with genres as keys and a list of aritst_ids as values
        """
        genre_dict = collections.defaultdict(list)
        for item in self.top_artists["items"]:
            # join list to string
            artist_genres = " ".join(item.get("genres"))
            artist_id = item.get("id")
            # not all all genres
            all_genres = [
                "pop", "metal", "k-pop", "hip hop", "rock", "indie", "rap",
                "alt z", "reggae", "low-fi"
            ]
            for genre in all_genres:
                if genre in artist_genres:
                    genre_dict[genre].append(artist_id)
            # also add related artists to genre dict
            for related_artist in self.spotipy_object.artist_related_artists(
                    artist_id)["artists"]:
                related_artist_id = related_artist.get("id")
                related_artist_genres = related_artist.get("genres")
                for genre in all_genres:
                    if genre in related_artist_genres:
                        genre_dict[genre].append(related_artist_id)
        self.genre_dict = genre_dict

    def get_top_tracks_of_artist_list(self, artist_list):
        """get list of top tracks (ids) from a list of artists

        Args:
            artist_list (list): list with artist_ids

        Returns:
            list: list with songs
        """
        song_list = []
        for artist in artist_list:
            tracks = self.spotipy_object.artist_top_tracks(artist_id=artist)
            for track in tracks["tracks"]:
                song_list.append(track.get("id"))
        return song_list

    def create_playlist(self,
                        n_songs=25,
                        genre=None,
                        n_artists=25,
                        save=False,
                        name=None):
        """creates a random playlist based in your top artists or selected genre

        Args:
            n_songs (int, optional): number of songs in the playlist. Defaults to 25.
            genre (_type_, optional): _description_. Defaults to None.
            n_artists (int, optional): number of top artists chosen. Defaults to 25.
            save (bool, optional): whether playlist should be saved in account. user_id must be specified in the object. Defaults to False.
            name (_type_, optional): name of playlist. if not specified (very) random 
            name is created. Defaults to None.


        Returns:
            list: list of track ids if not saved as playlist
        """
        self.artist_ranking = self.rank_artists()
        song_list = []

        # create playlist based on genre
        if genre is not None:
            if self.genre_dict is None:
                self.create_genre_dict()
            available_genres = self.genre_dict.keys()

            if genre not in available_genres:
                raise NameError(
                    genre +
                    " is not available, choose from following genres: " +
                    available_genres)
            #raise NotImplementedError("Creating a Playlist based on a genre has not been implemented yet")
            artists_of_genre = self.genre_dict.get(genre)
            song_list = self.get_top_tracks_of_artist_list(
                artist_list=artists_of_genre)

        # create playlist based on most popular artists
        else:
            # unnested Counter output with artist ids
            artist_list = [
                item[0] for item in self.artist_ranking.most_common(n_artists)
            ]
            song_list = self.get_top_tracks_of_artist_list(
                artist_list=artist_list)

        if len(song_list) < n_songs:
            n_songs = len(song_list)
            print("n_songs is to high, playlist will have " + n_songs +
                  " songs")
        tracks_list = random.choices(song_list, k=n_songs)

        # save or print songs
        if save == True:
            self.save_playlist(tracks_list=tracks_list, name=name)
        else:
            return tracks_list

    def save_to_json(self, filename):
        """save object of class listener to json 

        Args:
            filename (string): filename of json
        """
        # spotipy object can not be saved as json
        spotipy_object_tmp = self.spotipy_object
        spotipy_object_playlist_creation_tmp = self.spotipy_object_playlist_creation
        self.spotipy_object = "NULL"
        self.spotipy_object_playlist_creation = "NULL"
        with open(filename, "w") as f:
            json.dump(self.__dict__, f)

        self.spotipy_object = spotipy_object_tmp
        self.spotipy_object_playlist_creation = spotipy_object_playlist_creation_tmp

    @classmethod
    def load_json(cls, json_file):
        """loads json file into class

        Args:
            json_file (string): name of json file

        Returns:
            _type_: Object of class Listener
        """
        with open(json_file, 'r') as j:
            json_dict = json.loads(j.read())
        return cls(**json_dict)

    def print_top_artists_and_genres(self):
        """prints list with top generes and name of artist
        """
        genre_list = []
        for item in self.top_artists["items"]:
            genres = item.get("genres")
            l = [genres, item.get("name")]
            genre_list.append(l)
        print(genre_list)

    def playlist_based_on_single_song(self, songID=None, save_playlist=False):
        if songID is None:
            song = random.choice(self.top_tracks['items'])
            print("No song selected, choose random song: ", song.get("name"))
            songID = song.get("id")
        pass
