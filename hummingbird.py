from os import remove
from sys import stdin
import datetime
import random
import string
import threading

import config
from network import get_MAC, print_MAC_address
from music import MusicPlayer, get_random_song
from utils import log, generate_random_suffix, is_unknown_user

class User:
	def __init__(self, name=config.unknown_user_prefix, song=config.need_to_assign, length=config.time_max_song_length, arrival=datetime.datetime.now()):
		if is_unknown_user(name=name):
			self.name = name + generate_random_suffix()
		else:
			self.name = name
		if song == config.need_to_assign:
			self.song = get_random_song()
		else:
			self.song = song
		self.length = length
		self.arrival = arrival

	def has_not_played_today(self):
		# not played today if:
		# 	1) it's now after reset point and last played earlier today before reset point or earlier
		# 	2) it's now before reset point and last played earlier yesterday before reset point or earlier
		now = datetime.datetime.now()
		today = now.date()
		yesterday = today - datetime.timedelta(days=1)
		return (
			now.time() >= config.time_reset_time and self.arrival < datetime.datetime.combine(today, config.time_reset_time)
		) or (
			now.time() < config.time_reset_time and self.arrival < datetime.datetime.combine(yesterday, config.time_reset_time)
		)

	def queue_song(self, music_player):
		self.arrival = datetime.datetime.now()
		music_player.queue_song(user=self)

	def __unicode__(self):
		return "{name}: {song} ({length}s)".format(name=self.name, song=self.song, length=self.length)

class System:
	def __init__(self):
		log(message="Initializing...")
		self.music_player = MusicPlayer()
		self.all_addresses = self.read_in_addresses()
		self.waiting_for_input = False
		self.input_timeout()
		log(message="Waiting for tcpdump to provide input...")

		while True:
			# handle input as network traffic from tcpdump
			addresses = get_MAC(line=stdin.readline())
			self.waiting_for_input = False
			for address in addresses:
				# add address to dict
				self.add_new_address(address=address)
				user = self.all_addresses[address]
				print_MAC_address(address=address, user=user)

				# play the user's song (if theirs hasn't played already)
				if user.song != config.do_not_play and user.has_not_played_today():
					if not is_unknown_user(name=user.name) or config.play_unknowns:
						log(message="Detected activity from {name}.".format(name=user.name))
						user.queue_song(music_player=self.music_player)

	def input_timeout(self):
		if self.waiting_for_input:
			log(message="Warning: tcpdump has not provided input for a while. There may be something wrong.")
		else:
			self.waiting_for_input = True
			threading.Timer(interval=config.time_input_timeout, function=self.input_timeout).start()

	def read_in_addresses(self):
		addresses = {}

		lines = []
		# read in addresses from the current songs.csv
		with open(config.data_file, 'r') as f:
			for line in f.readlines():
				# get the user's information
				user_line = line.replace('\n','').split(',')
				if len(user_line) == 3:
					user_line.append(config.time_max_song_length)
				user_address, user_name, user_song, user_songlength = user_line
				user = User(name=user_name, song=user_song, length=user_songlength, arrival=datetime.datetime.utcfromtimestamp(0))

				# update the user's line and add to our dict
				lines.append(line.replace(config.need_to_assign, user.song))
				addresses[user_address] = user

		# rewrite the data file to handle changes (for NTAs)
		remove(config.data_file)
		with open(config.data_file, 'w') as f:
			f.writelines(lines)

		return addresses

	def add_new_address(self, address, user_name=config.unknown_user_prefix):
		# if the address is new, add it to our dict
		if address not in self.all_addresses:
			user = User(name=user_name)
			self.all_addresses[address] = user

			with open(config.data_file, 'a') as f:
				f.write("{address},{name},{song}\n".format(address=address, name=user.name, song=user.song))

			if is_unknown_user(name=user.name):
				log(message="A new unknown device with address {address} has been added and has been assigned {song}.".format(address=address, song=user.song))
			else:
				log(message="{name} has been added and has been assigned {song}.".format(name=user.name, song=user.song))

System()
