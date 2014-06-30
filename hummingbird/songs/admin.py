import os
import datetime
import random
import threading

from django.contrib import admin
from pygame import mixer

from hummingbird.settings import SOUND_DIR
import config
from utils import log
from songs.models import *

class SongManager:
	'''
	Music Player
	'''
	def init_mixer(self):
		mixer.init()
		self.play_sound(sound_name="hatching.wav")
		self.ready_to_queue = False
		self.user_song_currently_playing = None

		# clear queue by setting its played time to earlier than the queue time
		if config.clear_queue:
			for song in SongQueue.objects.filter(played__isnull=True):
				song.played = song.added - datetime.timedelta(seconds=1)
				song.save()

		# wait before queuing any songs
		if config.wait_to_play:
			time_wait_to_play = config.time_wait_to_play
		else:
			time_wait_to_play = 0
		threading.Timer(interval=time_wait_to_play, function=self.play_song_on_queue).start()

	def play_sound(self, sound_name):
		mixer.Sound(
			os.path.join(SOUND_DIR, sound_name)
		).play()

	def queue_song(self, user):
		if self.ready_to_queue:
			log(message="Waiting delay of {delay} seconds to queue {user}'s song.".format(delay=user.userprofile.delay, user=user))
			self.play_sound(sound_name="activity.wav")
			threading.Timer(user.userprofile.delay, self.queue_song_after_delay, [user.userprofile.walkin_song]).start()

	def queue_song_after_delay(self, song):
		SongQueue.objects.create(song=song)
		log(message="Queued {song}.".format(song=song.song))

	def play_song_on_queue(self):
		if not self.ready_to_queue:
			self.ready_to_queue = True
			log(message="System now ready to play walk-in songs.")
			mixer.stop()
			self.play_sound(sound_name="ready.wav")

		if not mixer.music.get_busy():
			song_queue = SongQueue.objects.filter(played__isnull=True)
			if song_queue:
				# get the first song on the queue
				song_to_play_queue = song_queue[0]
				song_to_play_queue.played = datetime.datetime.now()
				song_to_play_queue.save()
				song_to_play_assignment = song_to_play_queue.song
				song_to_play_song = song_to_play_assignment.song
				# set the user of the currently playing song
				user_to_play = song_to_play_assignment.user
				self.user_song_currently_playing = user_to_play
				# set a timer for long songs
				threading.Timer(song_to_play_assignment.walkin_length, self.stop_long_song, [user_to_play]).start()
				# play the song
				log(message="Playing {song}.".format(song=song_to_play_assignment))
				try:
					mixer.music.load(song_to_play_song.audiofile.file)
					mixer.music.play()
				except:
					log(message="Hummingbird failed to play {song}.".format(song=song_to_play_assignment))
			else:
				self.user_song_currently_playing = None

		threading.Timer(interval=config.time_check_queue, function=self.play_song_on_queue).start()

	def stop_long_song(self, user):
		if self.user_song_currently_playing == user:
			mixer.music.fadeout(config.time_fadeout_song)

	'''
	Song Manager
	'''
	def add_uploaded_song(self, title, audiofile, artist="n/a", album="n/a", random=False):
		song, created = Song.objects.get_or_create(title=title, audiofile=audiofile, artist=artist, album=album, random=random)
		return song

	def assign_walkin_song(self, user, song, walkin_length=config.time_default_max_song_length):
		sa, created = SongAssignment.objects.get_or_create(user=user, song=song)
		sa.walkin_length = walkin_length
		sa.save()
		user.walkin_song = sa
		user.save()

	def assign_random_song(self, user):
		random_list = Song.objects.filter(random=True)
		if len(random_list) == 0:
			raise AssertionError("A random song could not be assigned because there are no random songs in the system.")
		self.assign_walkin_song(user=user, song=random.choice(random_list))
	