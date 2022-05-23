# mkply

Create a Spotify Playlist for yourself or a joint playlist with your friends. 

This package is a wrapper around [Spotipy](https://github.com/plamere/spotipy).

## Installation

```bash
$ pip install git+https://github.com/elena-krismer/mkply.git

```

## Usage

<details>
  <summary>User Authenification</summary>

* get `client_id` and `client_secret`  https://developer.spotify.com/documentation/general/guides/authorization/app-settings/

* specify `redirect_uri` in your spotify developer account

* Plus, to save your playlist you require your `user_id`, which you can find in your Spotify account (-> account)

More details about the authorization you can find on [Spotipy](https://github.com/plamere/spotipy).

</details>


<details>
  <summary>Create playlist for myself</summary>

```python
import mkply
sp = mkply.Listener(client_id="your_client_id",
                             client_secret="your_client_secret",
                             redirect_uri = "your_redirect_uri", 
                             user_id = "your_user_id")
sp.create_playlist(save = True)
```
  
</details>


<details>
  <summary>Create playlist with friends</summary>

 
```python
import mkply
friend_1 = mkply.Listener(client_id="friend_1_client_id",
                             client_secret="friend_1_client_secret",
                             redirect_uri = "friend_1_redirect_uri")
friend_2 = mkply.Listener(client_id="friend_2_client_id",
                             client_secret="friend_2_client_secret",
                             redirect_uri = "friend_2_redirect_uri") 

# Spotify main account - here playlists will be saved
main_account = mkply.Listener(client_id="your_client_id",
                             client_secret="your_client_secret",
                             redirect_uri = "your_redirect_uri", 
                             user_id = "your_user_id")

sp = mkply.MultiListener(list_of_listeners = [friend_1, friend_2, main_account] , spotify_account = main_account)             
sp.create_playlist(save = True)
```
  
</details>



## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`mkply` was created by Elena Krismer. It is licensed under the terms of the MIT license.

## Credits

`mkply` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
