import collections
#from gc import collect
#from logging import warning
#from tokenize import Name
import spotipy
from collections import Counter
import randomname
import random
import warnings


class MultiListener:
    def __init__(self, list_of_listeners, spotify_account):
        """Object containing information for multiple Listener used to 
        create common playlist for all listeners

        Args:
            list_of_listeners (_type_): a list of objects of class Listener
            spotify_account (_type_): a object of class Listener 
            this account will be used to save playlists
        """
        self.list_of_listeners = list_of_listeners
        self.main_user = spotify_account # to save Playlist and get spotify connection
        self.artist_ranking = self.rank_artists()
        self.genre_dict = None
        if self.main_user.spotipy_object_playlist_creation is None:
            warnings.warn("User_id for in spotify_account is missing. playlist creation will not be possible.")


    def rank_artists(self):
        """Creates a dict with the ranking of the artists. Highest ranked artist should be the most popular
        among listeners. This is based on the top aritist of the Listener. If Listener like the same artist
        the count will be increased by 2, if Listener likes an artist related artist the count will be increased
        by 1.
        Weakness: Is very depending on the distrubition of artists of listeners. Ranking can be created in favour
        of one Listener (if Listener is listing heavily one genre and to artist related artists)

        Returns:
            _type_: Counter dict with artist_id as key and value is the count/ranking of the artist
        """
        ranked_artists_dict = Counter()
        # get top artist for each Listener object
        for listener in self.list_of_listeners:
            for item in listener.top_artists["items"]:
                # get the artist id
                artist_id = item.get("id")
                if artist_id in ranked_artists_dict:
                    ranked_artists_dict[artist_id] =  ranked_artists_dict.get(artist_id) + 2
                else: 
                    ranked_artists_dict[artist_id] =  2  
                # get related artists increase by 1
                for related_artist in self.main_user.spotipy_object.artist_related_artists(artist_id)["artists"]:
                    related_artist_id = related_artist.get("id")
                    if related_artist_id in ranked_artists_dict:
                        ranked_artists_dict[related_artist_id] =  ranked_artists_dict.get(related_artist_id) + 1
                    else:
                        ranked_artists_dict[related_artist_id] =  1   
        return ranked_artists_dict


    def create_genre_dict(self):
        """create dict with genres as keys and a list of aritst_ids as values
        """
        genre_dict = collections.defaultdict(list)
        # not all all genres
        all_genres = ["pop", "metal","k-pop", "hip hop", "rock", "indie", "rap", "alt z",
                "reggae", "low-fi"]
        for listener in self.list_of_listeners:
            for item in listener.top_artists["items"]:
                # join list to string
                artist_genres = " ".join(item.get("genres"))
                artist_id = item.get("id")
                for genre in all_genres:
                    if genre in artist_genres:
                        genre_dict[genre].append(artist_id)
                # also add related artists to genre dict
                for related_artist in self.main_user.spotipy_object.artist_related_artists(artist_id)["artists"]:
                    related_artist_id = related_artist.get("id")
                    related_artist_genres = related_artist.get("genres")
                    for genre in all_genres:
                        if genre in related_artist_genres:
                            genre_dict[genre].append(related_artist_id)
  
        self.genre_dict = genre_dict


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
        playlist = self.main_user.spotipy_object_playlist_creation.user_playlist_create(user =self.main_user.user_id, name =name, public=True, collaborative=False, description='')
        self.main_user.spotipy_object_playlist_creation.playlist_add_items(playlist_id = playlist.get("id"), items = tracks_list, position=None)
        print("Playlist: " + name + " has been saved")
        print("Playlist can be found here: ", playlist.get("external_urls").get("spotify"))


    def create_features_df(self):
        pass

    
    def save_to_json(self, filename):
        """save object of class listener to json 

        Args:
            filename (string): filename of json
        """
        with open(filename, 'w') as f:
            json.dumps(self.__dict__, f) #default=vars


    @classmethod
    def load_json(cls, json_file):
        """loads json file into class

        Args:
            json_file (string): name of json file

        Returns:
            _type_: Object of class Listener
        """
        json_dict = json.loads(json_file)
        return cls(**json_dict)


    def create_playlist(self, n_songs = 25, genre = None, n_artists = 25, save = False, name = None):
        """creates a random playlist based in your top artists (atm) or selected genre

        Args:
            n_songs (int, optional): number of songs in the playlist. Defaults to 25.
            genre (_type_, optional): _description_. Defaults to None.
            n_artists (int, optional): number of top artists chosen. Defaults to 25.
            save (bool, optional): whether playlist should be saved in account. user_id must be specified in the object. Defaults to False.
            name (_type_, optional): name of playlist. if not specified (very) random 
            name is created. Defaults to None.

        Returns:
            _type_: _description_
        """
        self.artist_ranking = self.rank_artists()
        song_list = []

        # create playlist based on genre
        if genre is not None:
            if self.genre_dict is None:
                self.create_genre_dict()
            available_genres = self.genre_dict.keys()

            if genre not in available_genres:
                raise NameError(genre  + " is not available, choose from following genres: " + available_genres)
        
            artists_of_genre = self.create_genre_dict.get(genre)
            song_list = self.get_top_tracks_of_artist_list(artist_list= artists_of_genre)
        
        # create playlist based on most popular artists
        else:
            # unnested Counter output with artist ids
            artist_list = [item[0] for item in self.artist_ranking.most_common(n_artists)]
            song_list = self.get_top_tracks_of_artist_list(artist_list= artist_list)
        
        if len(song_list) < n_songs:
            n_songs = len(song_list)
            print("n_songs is to high, playlist will have " + n_songs + " songs")
        tracks_list = random.choices(song_list, k=n_songs)

        # save or print songs
        if save == True:
            self.save_playlist(tracks_list = tracks_list, name = name)
        else:
            return tracks_list