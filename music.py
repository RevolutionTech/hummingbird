from os import listdir
import random
import threading

from pygame import mixer

import config

def get_random_song():
	randomDir = config.audio_bytes_dir + config.random_subdir
	return "{directory}{file}".format(directory=randomDir, file=random.choice(listdir(randomDir)))

class MusicPlayer:
	def __init__(self):
		mixer.init()
		self.song_queue = []
		self.play_song_on_queue()

	def play_song_on_queue(self):
		threading.Timer(0.25, self.play_song_on_queue).start()

		if self.song_queue and not mixer.music.get_busy():
			user_name, user_song = self.song_queue[0]
			self.song_queue = self.song_queue[1:]
			print "Playing {name}'s song {song}.".format(name=user_name, song=user_song)
			mixer.music.load(user_song)
			mixer.music.play()

	def queue_song(self, name, songfile):
		self.song_queue.append((name, songfile))