#!/usr/bin/env python3
import logging
import os
import pprint
import sys
import time

import mpv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

played_videos = 1
amount_of_videos = len(os.listdir("./coubs"))

def my_log(loglevel, component, message):
	print('{} - [{}]: {}'.format(component, loglevel, message))

logging.basicConfig(format='%(asctime)s - %(name)s - [%(levelname)s]: %(message)s',
					level=logging.INFO)

logger = logging.getLogger(__name__)
player = mpv.MPV()


player.fullscreen = True
player.loop = True
# Option access, in general these require the core to reinitialize
# player['vo'] = 'sdl'


@player.on_key_press('RIGHT')
def next_video():
	global played_videos, player
	try:
		if player.playlist_next():
			played_videos += 1
	except:
		logger.info("-->Moving to first video-->")
		player.stop()
		player = mpv.MPV()
		player.fullscreen = True
		player.loop = True
		get_videos_to_playlist()
		player.playlist_shuffle()
		player.playlist_pos = 0
		player.wait_until_playing()



@player.on_key_press('LEFT')
def prev_video():
	global played_videos
	try:
		if player.playlist_prev():
			played_videos += 1
	except:
		logger.info("<--Moving to last video<--")
		player.playlist_play_index(len(os.listdir("./coubs")) - 1)
		played_videos += 1
	


@player.on_key_press('q')
def exit_player():
	player.stop()
	os._exit(0)


@player.on_key_press('ESC')
def turn_off_fullscreen():
	player.fullscreen = False


@player.on_key_press('f')
@player.on_key_press('F')
def switch_fullscreen():
	if player.fullscreen:
		player.fullscreen = False
	else:
		player.fullscreen = True


@player.on_key_press('s')
def shuffle():
	player.playlist_shuffle

def get_videos_to_playlist():
	for video_title in os.listdir("./coubs"):
		player.playlist_append(f"./coubs/{video_title}")

@player.on_key_press('a')
def get_new_videos_to_playlist():
	logger.info(player.playlist_filenames)
	player.playlist_play_index(0)
	player.playlist_clear()
	logger.info(player.playlist_filenames)
	for video_title in os.listdir("./coubs"):
		if video_title == os.listdir("./coubs")[0]:
			continue
		player.playlist_append(f"./coubs/{video_title}")
	player.playlist_play_index(0)
	logger.info(player.playlist_filenames)
	shuffle()
	logger.info(player.playlist_filenames)

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

def check_music_activity():
	wait_seconds = 0
	while not sp.current_user_playing_track()["is_playing"]:
		if wait_seconds % 30 == 0:
			logger.info("Waiting for playing music")
		time.sleep(1)
		wait_seconds += 1

def check_video_activity():
	global played_videos, amount_of_videos
	real_amount_of_videos = len(os.listdir("./coubs"))

	if played_videos == real_amount_of_videos:
		if amount_of_videos != real_amount_of_videos:
			amount_of_videos = real_amount_of_videos
			get_new_videos_to_playlist()


get_videos_to_playlist()
player.playlist_shuffle()

player.playlist_pos = 0
player.wait_until_playing()

scope = "user-read-currently-playing"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

check_music_activity()
current_track_id = get_current_track()['id']


while True:

	check_video_activity()
	check_music_activity()
	try:
		current_track_info = get_current_track()
	except:
		time.sleep(0.5)

	if current_track_info['id'] != current_track_id:
			pprint.pprint(
				current_track_info,
				indent=3
			)
			current_track_id = current_track_info['id']
			next_video()
	time.sleep(0.5)
