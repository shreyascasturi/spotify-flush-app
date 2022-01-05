"""
Prerequisites
    pip3 install spotipy Flask Flask-Session
    // from your [app settings](https://developer.spotify.com/dashboard/applications)
    export SPOTIPY_CLIENT_ID=client_id_here
    export SPOTIPY_CLIENT_SECRET=client_secret_here
    export SPOTIPY_REDIRECT_URI='http://127.0.0.1:8080' // must contain a port
    // SPOTIPY_REDIRECT_URI must be added to your [app settings](https://developer.spotify.com/dashboard/applications)
    OPTIONAL
    // in development environment for debug output
    export FLASK_ENV=development
    // so that you can invoke the app outside of the file's directory include
    export FLASK_APP=/path/to/spotipy/examples/app.py
 
    // on Windows, use `SET` instead of `export`
Run app.py
    python3 app.py OR python3 -m flask run
    NOTE: If receiving "port already in use" error, try other ports: 5000, 8090, 8888, etc...
        (will need to be updated in your Spotify app and SPOTIPY_REDIRECT_URI variable)

NOTES: Taken from plamere/spotipy examples folder, labeled app.py. Changes were made to add functionality.
"""

import os
from flask import Flask, session, request, redirect
from flask_session import Session
import spotipy
import uuid
from pprint import pprint

app = Flask(__name__)

# why is this needed?
# is it to give each connecting session uniqueness?
app.config['SECRET_KEY'] = os.urandom(64)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
Session(app)

# cache is needed to store authentication tokens
# during a session, I think.
caches_folder = './.spotify_caches/'
if not os.path.exists(caches_folder):
   os.makedirs(caches_folder)

def session_cache_path():
   return caches_folder + session.get('uuid')

@app.route('/')
def index():
    if not session.get('uuid'):
        # Step 1. Visitor is unknown, give random ID
        session['uuid'] = str(uuid.uuid4())

    # basic process: create a cache handler for token
    # create the auth_manager object (probably uses the variables that we exported/set)
    # auth manager gives you authorization url to go to
    # you can get the token as necessary
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope='user-read-currently-playing user-library-read playlist-modify-private',
                                                cache_handler=cache_handler, 
                                                show_dialog=True)

    if request.args.get("code"):
        # Step 3. Being redirected from Spotify auth page
        auth_manager.get_access_token(request.args.get("code"))
        return redirect('/')

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        # Step 2. Display sign in link when no token
        auth_url = auth_manager.get_authorize_url() # how is this url given?
        return f'<h2><center><a href="{auth_url}">Sign in</a></center></h2>'

    # Step 4. Signed in, display data
    #return "LOOKS LIKE THIS WORKS?"
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    return f'<h2>Hi {spotify.me()["display_name"]}, ' \
           f'<small><a href="/sign_out">[sign out]<a/></small></h2>' \
           f'<a href="/playlists">my playlists</a> | ' \
           f'<a href="/currently_playing">currently playing</a> | ' \
        	   f'<a href="/current_user">me</a> | ' \
                   f'<a href="/snapshot">snapshot<a/> | '\
                   f'<a href="/test_multiple_authors"test_multiple_authors<a/>'


# @app.route('/sign_out')
# def sign_out():
#     try:
#         # Remove the CACHE file (.cache-test) so that a new user can authorize.
#         os.remove(session_cache_path())
#         session.clear()
#     except OSError as e:
#         print ("Error: %s - %s." % (e.filename, e.strerror))
#     return redirect('/')

# give snapshot functionality here
# first, print all albums out now.

@app.route('/test_multiple_authors')
def test_mult_authors():
   
   
@app.route('/snapshot')
def snapshot():
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')

    spotify = spotipy.Spotify(auth_manager=auth_manager)

    offset_test = 0
    saved_albums_tuple_list = []
    
    while offset_test != 500:
       
       saved_albums_raw = spotify.current_user_saved_albums(limit=20, offset=offset_test)
       for item in saved_albums_raw["items"]:
          saved_albums_tuple_list.append((item["album"]["name"], item["album"]["artists"][0]["name"]))
       offset_test += 20

    Album: dict_keys(['href', 'items', 'limit', 'next', 'offset', 'previous', 'total'])[return to home]

    for item in saved_albums_raw["items"]:
       print("item is: " + str(item["album"]))

       
    return f'Albums: {saved_albums_tuple_list}' \
        f'<a href="/">[return to home]<a/>'
    #return spotify.current_user_saved_albums(limit=1)
#    return f'<a href="/">[return to home]<a/>'

@app.route('/playlists')
def playlists():
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')

    spotify = spotipy.Spotify(auth_manager=auth_manager)
    return spotify.current_user_playlists()


# @app.route('/currently_playing')
# def currently_playing():
#     cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
#     auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
#     if not auth_manager.validate_token(cache_handler.get_cached_token()):
#         return redirect('/')
#     spotify = spotipy.Spotify(auth_manager=auth_manager)
#     track = spotify.current_user_playing_track()
#     if not track is None:
#         return track
#     return "No track currently playing."


# @app.route('/current_user')
# def current_user():
#     cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
#     auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
#     if not auth_manager.validate_token(cache_handler.get_cached_token()):
#         return redirect('/')
#     spotify = spotipy.Spotify(auth_manager=auth_manager)
#     return spotify.current_user()


'''
Following lines allow application to be run more conveniently with
`python app.py` (Make sure you're using python3)
(Also includes directive to leverage pythons threading capacity.)
'''
# if __name__ == '__main__':
#     app.run(threaded=True, port=int(os.environ.get("PORT",
#                                                    os.environ.get("SPOTIPY_REDIRECT_URI", 5000).split(":")[-1])))
