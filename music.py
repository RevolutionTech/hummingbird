from os import listdir
import random
import threading

from pygame import mixer

import config

def get_random_song():
	randomDir = config.audio_dir + config.random_subdir
	return "{directory}{file}".format(directory=randomDir, file=random.choice(listdir(randomDir)))

class MusicPlayer:
	def __init__(self):
		mixer.init()
		self.ready_to_queue = False
		self.song_queue = []
		self.user_song_currently_playing = None
		threading.Timer(interval=config.time_wait_to_play, function=self.play_song_on_queue).start()

	def play_song_on_queue(self):
		if not self.ready_to_queue:
			self.ready_to_queue = True
			print "System now ready to play walk-in songs."
		threading.Timer(interval=config.time_check_queue, function=self.play_song_on_queue).start()

		if not mixer.music.get_busy():
			if self.song_queue:
				user_name, user_song = self.song_queue[0]
				self.song_queue = self.song_queue[1:]
				self.user_song_currently_playing = user_name
				print "Playing {name}'s song {song}.".format(name=user_name, song=user_song)
				threading.Timer(config.time_max_song_length, self.stop_long_song, [user_name]).start()
				mixer.music.load(user_song)
				mixer.music.play()
			else:
				self.user_song_currently_playing = None

	def stop_long_song(self, user):
		if self.user_song_currently_playing == user:
			mixer.music.fadeout(config.time_fadeout_song)

	def queue_song(self, user_name, user_song):
		if self.ready_to_queue:
			print "Queued {name}'s song {song}.".format(name=user_name, song=user_song)
			self.song_queue.append((user_name, user_song))
