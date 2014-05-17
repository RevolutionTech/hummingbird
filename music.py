from os import listdir
import random
import threading

from pygame import mixer

import config
from utils import log

def listdir_nohidden(path):
	return [x for x in listdir(path) if not x.startswith('.')]

def get_random_song():
	randomDir = config.audio_dir + config.random_subdir
	return "{directory}{file}".format(directory=randomDir, file=random.choice(listdir_nohidden(randomDir)))

class MusicPlayer:
	def __init__(self):
		mixer.init()
		self.ready_to_queue = False
		self.song_queue = []
		self.user_song_currently_playing = None

		# wait before queuing any songs
		if config.wait_to_play:
			time_wait_to_play = config.time_wait_to_play
		else:
			time_wait_to_play = 0
		threading.Timer(interval=time_wait_to_play, function=self.play_song_on_queue).start()

	def play_song_on_queue(self):
		if not self.ready_to_queue:
			self.ready_to_queue = True
			log(message="System now ready to play walk-in songs.")
		threading.Timer(interval=config.time_check_queue, function=self.play_song_on_queue).start()

		if not mixer.music.get_busy():
			if self.song_queue:
				# pop the next song off of the front of the queue
				user = self.song_queue[0]
				self.song_queue = self.song_queue[1:]
				# set the user of the currently playing song
				self.user_song_currently_playing = user.name
				# set a timer for long songs
				threading.Timer(user.length, self.stop_long_song, [user.name]).start()
				# play the song
				log(message="Playing {name}'s song {song}.".format(name=user.name, song=user.song))
				mixer.music.load(user.song)
				mixer.music.play()
			else:
				self.user_song_currently_playing = None

	def stop_long_song(self, user_name):
		if self.user_song_currently_playing == user_name:
			mixer.music.fadeout(config.time_fadeout_song)

	def queue_song(self, user):
		if self.ready_to_queue:
			log(message="Queued {name}'s song {song}.".format(name=user.name, song=user.song))
			self.song_queue.append(user)
