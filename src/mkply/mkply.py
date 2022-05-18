from email.mime import base
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

urn = 'spotify:artist:3jOstUTkEu2JkjvRdBA5Gu'
sp = spotipy.Spotify()


class SingleListener:
    # wrappe for spotipy library
    def __init__(self):
        self.clientID = None
        self.credentials = None
    def playlist_based_on_single_song(self, songID, save_playlist = False):
        pass

class MultiListener:
    def __init__(self):
        self.artists= None # dict with name of listener and artist 
        self.favourite_song = None # dict with name of listener and favourtie_song
        self.main_user = None # to save Playlist
    def
      
    
    
      

def calculate_distance():
    # calculate euclidean distance between one song from group A and other groups
    # take songs with smallest euclidean distance
    pass


def playlist_based_on_playlists(list_of_pl, based_on = ["artists", "features"], length = 25):
    """one user is sufficient finds intersect between several playlists

    Args:
        list_of_pl (_type_): _description_
        based_on (list, optional): _description_. Defaults to ["artists", "features", "genre"].
        length (int, optional): _description_. Defaults to 25.
    """
    # get playlists
    for pl in list_of_pl:
        sp.playlist(playlist_id = pl, fields=None, market=None, additional_types=('track', ))
        # but songs into df with featues
    if based_on == "features":
        # find most similar songs of the playlists using features like energy,...
        calculate_distance()
        pl = []
    if based_on == "artists":
        # get artists and artist related artists   
        # use counting
        pl = []
    pass



def create_multiple_userplaylist(userIDs,  pl_length,
    based_on = ["recently_played", "artists", "genre"]):
    """needs to connect to the spotify of multiple users

    Args:
        userIDs (_type_): _description_
        pl_length (_type_): _description_
        based_on (list, optional): _description_. Defaults to ["recently_played", "artists", "genre"].

    Raises:
        ValueError: _description_
    """
    if based_on == "artists":
        # create list of songs
        songs = []
        # get artists each user is following 
        # either get top_artists for each user or all artists which the user is following
        # count how often artist occurs + 1 
        # get artist_related_artists + 0.5 
        # using func: sp.artist_related_artists(artist_id)
        # select artists with highest count get top songs of those 
        # concate all songs and select n songs
        pl = songs.random(pl_length)
    elif based_on == "saved_tracks":
        # use func: current_user_saved_tracks(limit=20, offset=0, market=None)
        pl = []
    elif based_on == "top_tracks":
        # use func: current_user_top_tracks(limit=20, offset=0, time_range='medium_term')
        pl = []
    else:
        raise ValueError 

    pass


def create_pl_for_users_genre(userIDs, categoryID):
    # get playlists for specific category 
    sp.category_playlists(category_id=categoryID, country=None, limit=20, offset=0)




