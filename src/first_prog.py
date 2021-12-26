# imports needed
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
import os
#from pprint import pprint
# Create a client to use Spotify API
# uses spotify-given client id and client secrets
# this data is given when you register app with spotify.
def auth_enable():
    # sp_user = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id,
    #                                                     redirect_uri="localhost:5000",
    #                                                     scope="playlist-read-private",
    #                                                     open_browser=True))
    # me = sp_user.me();
    # pprint(me)
    print(os.environ.get('SPOTIPY_CLIENT_ID'))
    print(os.environ.get('SPOTIPY_CLIENT_SECRET'))
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=os.environ.get('SPOTIPY_CLIENT_ID'),
                                                              client_secret=os.environ.get('SPOTIPY_CLIENT_SECRET')))
    return sp
    #sp = spotipy.Spotify()



# main method.
# connects to spotify. Gets first 20 tracks of weezer.
def main():
    print("hello world")
    sp = auth_enable()
    results = sp.search(q='weezer', limit=20)
    for i, t in enumerate(results['tracks']['items']):
        print(' ', i, t['name'])

main()
