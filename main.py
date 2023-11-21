import spotipy
import random
from spotipy.oauth2 import SpotifyOAuth


#############################################################
# GET ALL PLAYLIST NAME
#############################################################

print("Welcome to the spotify playlist script!")
print("Put 'finish' in input for finish playlist name")

PLAYLIST_NAMES = []
loop = True

while loop:
    name = input("Put a playlist name (): ")

    if name == "finish":
        break

    PLAYLIST_NAMES.append(name)


#############################################################
# CONNECT TO SPOTIFY API
#############################################################

SPOTIPY_CLIENT_ID = '' # put client id of your spotify dev API
SPOTIPY_CLIENT_SECRET = '' # put secret client of your spotify dev API
SPOTIPY_REDIRECT_URI = 'https://google.com'

# Initialize the Spotify API client
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope="playlist-modify-public playlist-read-private"
    )
)


#############################################################
# DELETE ALL MUSIC IN MAIN PLAYLIST
#############################################################

results = sp.current_user_playlists()

for playlist in results.get('items'):
    
    if playlist.get('name') == "": # put main playlist name
        
        playlistId = playlist.get('id')
        tracks = sp.playlist_tracks(playlistId)
        track_uris = [track['track']['uri'] for track in tracks['items']]
        for uri in track_uris:
            sp.playlist_remove_all_occurrences_of_items(playlistId, [uri])


#############################################################
# GET ALL MUSIC IN EACH PLAYLIST AND SHUFFLE ALL
#############################################################

ALL_MUSIC_URI_TRACK = []

for playlist in results.get('items'):
    for playlist_name in PLAYLIST_NAMES:
        if playlist.get('name') == playlist_name:
            playlistId = playlist.get('id')
            tracks = sp.playlist_tracks(playlistId)

            for music in tracks['items']:
                ALL_MUSIC_URI_TRACK.append(music['track']['uri'])

random.shuffle(ALL_MUSIC_URI_TRACK)


#############################################################
# ADD ALL MUSIC TO MAIN PLAYLIST
#############################################################

playlist_name = '' # put main playlist name
playlist_id = None
playlists = sp.current_user_playlists()

for playlist in playlists['items']:
    if playlist['name'] == playlist_name:
        playlist_id = playlist['id']
        break

sp.playlist_add_items(playlist_id, ALL_MUSIC_URI_TRACK)

