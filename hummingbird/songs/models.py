from django.db import models

import config

class Song(models.Model):
	title = models.CharField(max_length=config.song_title_max_length)
	artist = models.CharField(max_length=config.song_artist_max_length, default="n/a")
	album = models.CharField(max_length=config.song_album_max_length, default="n/a")
	random = models.BooleanField(default=False, db_index=True)

	def __unicode__(self):
		return "{title} by {artist}".format(title=self.title, artist=self.artist)

	def isRandom(self):
		return self.random

class SongAssignment(models.Model):
	user = models.ForeignKey('users.UserProfile')
	song = models.ForeignKey(Song)
	walkin_length = models.IntegerField(default=config.time_default_max_song_length)

	def __unicode__(self):
		return "{user}\'s song {song}".format(user=self.user.user, song=self.song)

class SongQueue(models.Model):
	song = models.ForeignKey(SongAssignment)
	added = models.DateTimeField(auto_now_add=True, blank=True)
	played = models.DateTimeField(null=True, blank=True, db_index=True)

	def __unicode__(self):
		return "{song} queued at {added}".format(song=self.song, added=self.added)
