from os import remove
from sys import stdin
import random
import string
import threading

import config
from network import get_MAC
from music import MusicPlayer, get_random_song
from utils import generate_random_suffix, is_unknown_user

class System:
	def __init__(self):
		print "Initializing..."

		self.reset_system()
		self.all_addresses = self.read_in_addresses()

		print "Waiting for tcpdump to provide input..."

		while True:
			# handle input as network traffic from tcpdump
			addresses = get_MAC(line=stdin.readline())
			for address in addresses:
				self.add_new_address(address=address)
				user_name, user_song = self.all_addresses[address]
				# play the user's song (if theirs hasn't played already)
				if user_song != config.do_not_play and address not in self.addresses_played_today:
					self.addresses_played_today.add(address)
					if not is_unknown_user(user_name=user_name) or config.play_unknowns:
						print "Detected activity from {name}.".format(name=user_name)
						self.music_player.queue_song(user_name=user_name, user_song=user_song)

	def reset_system(self):
		# reset (or initialize) the system
		threading.Timer(interval=config.time_reset_system, function=self.reset_system).start()
		self.music_player = MusicPlayer()
		self.addresses_played_today = set()

		print "System has been initialized/reset."

	def read_in_addresses(self):
		addresses = {}

		lines = []
		# read in addresses from the current songs.csv
		with open(config.data_file, 'r') as f:
			for line in f.readlines():
				# get the user's information
				user_address, user_name, user_song = line.replace('\n','').split(',')

				# assign a random song, if needed
				if user_song == config.need_to_assign:
					user_song = get_random_song()
					lines.append(line.replace(config.need_to_assign, user_song))
				else:
					lines.append(line)

				# add to our dict
				addresses[user_address] = (user_name, user_song)

		# rewrite the data file to handle changes (for NTAs)
		remove(config.data_file)
		with open(config.data_file, 'w') as f:
			f.writelines(lines)

		return addresses

	def add_new_address(self, address, user_name=config.unknown_user_prefix):
		# if the address is new, add it to our dict
		if address not in self.all_addresses:
			if is_unknown_user(user_name=user_name):
				user_name += generate_random_suffix()

			randomSong = get_random_song()

			with open(config.data_file, 'a') as f:
				f.write("{address},{name},{song}\n".format(address=address, name=user_name, song=randomSong))
			self.all_addresses[address] = (user_name, randomSong)

			if is_unknown_user(user_name=user_name):
				print "A new unknown device with address {address} has been added and has been assigned {song}.".format(address=address, song=randomSong)
			else:
				print "{name} has been added and has been assigned {song}.".format(name=user_name, song=randomSong)

System()
