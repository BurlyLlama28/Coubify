from pprint import pprint
import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "user-read-currently-playing"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))


def get_current_track():
	json_resp = sp.current_user_playing_track()

	track_id = json_resp['item']['id']
	track_name = json_resp['item']['name']
	artists = [artist for artist in json_resp['item']['artists']]

	artist_names = ', '.join([artist['name'] for artist in artists])

	current_track_info = {
		"id": track_id,
		"track_name": track_name,
		"artists": artist_names,
	}

	return current_track_info

current_track_id = get_current_track()['id']

current_track_info = get_current_track()
pprint(
    current_track_info,
    indent=3
)
current_track_id = current_track_info['id']