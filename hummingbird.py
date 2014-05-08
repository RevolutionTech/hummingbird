from os import remove
from sys import stdin
import random
import string

import config
from network import get_MAC
from music import MusicPlayer, get_random_song
from utils import generate_random_suffix, is_unknown_user

def read_in_addresses():
	addresses = {}

	lines = []
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

	remove(config.data_file)

	with open(config.data_file, 'w') as f:
		f.writelines(lines)

	return addresses

def add_new_address(address, name=config.unknown_user_prefix):
	if address not in all_addresses:
		if is_unknown_user(name):
			name += generate_random_suffix()

		randomSong = get_random_song()

		with open("songs.csv", 'a') as f:
			f.write("{address},{name},{song}\n".format(address=address, name=name, song=randomSong))
		all_addresses[address] = (name, randomSong)

		if is_unknown_user(name):
			print "A new unknown device with address {address} has been added and has been assigned {song}.".format(address=address, song=randomSong)
		else:
			print "{name} has been added and has been assigned {song}.".format(name=name, song=randomSong)

print "Initializing..."

music_player = MusicPlayer()
all_addresses = read_in_addresses()
addresses_played_today = set()

print "Waiting for tcpdump to provide input..."

while True:
	# handle input as network traffic from tcpdump
	addresses = get_MAC(stdin.readline())
	for address in addresses:
		add_new_address(address)
		user_name, user_song = all_addresses[address]
		if user_song != config.do_not_play and address not in addresses_played_today:
			addresses_played_today.add(address)
			print "Queued {name}'s song {song}.".format(name=user_name, song=user_song)
			music_player.queue_song(user_name, user_song)