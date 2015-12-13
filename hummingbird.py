import datetime
import threading
from sys import stdin

import ast
import requests
import random
import string
from os import remove

import config
from network import get_MAC, print_MAC_address
from music import MusicPlayer
from utils import log, generate_random_suffix, is_unknown_user


class User:
    def __init__(self, system, name=config.unknown_user_prefix, song=config.need_to_assign, length=config.time_max_song_length, arrival=datetime.datetime.now()):
        if is_unknown_user(name=name):
            self.name = name + generate_random_suffix()
        else:
            self.name = name
        if song == config.need_to_assign:
            self.song = system.music_player.get_random_song()
        else:
            self.song = song
        self.length = length
        self.arrival = arrival

    def has_not_played_today(self):
        # not played today if:
        #   1) it's now after reset point and last played earlier today before reset point or earlier
        #   2) it's now before reset point and last played earlier yesterday before reset point or earlier
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
        # local_payload_cache uses mac_id ("address") as key, with the value being a dictionary of mac_id and datetime value of last time the api was pinged.
        # Cache is only used if use_cache is set to True in config.py
        self.local_payload_cache = {}       
        self.music_player = MusicPlayer()
        self.waiting_for_input = False
        self.input_timeout()
        log(message="Waiting for tcpdump to provide input...")

        while True:
            # handle input as network traffic from tcpdump
            addresses = get_MAC(line=stdin.readline())
            self.waiting_for_input = False
            for address in addresses:
                
                ## Pings Hummingbird Django server. If use_cache is set to True, use self.local_payload_cache as a cache.
                if config.use_cache:
                    if address.lower() in self.local_payload_cache:
                        # payload is a tuple of address and last_checked_datetime
                        payload = self.local_payload_cache[address.lower()]
                        # Set a 60 second cache             
                        if (datetime.datetime.now() - payload['last_sent_dt']).seconds > config.cache_time_seconds:
                            r = requests.get("http://127.0.0.1:8000/hummingbird/build_user_from_device/", params=payload)
                            payload['last_sent_dt'] = datetime.datetime.now()
                            self.local_payload_cache[address.lower()] = payload
                            cached = False
                        else:
                            cached = True
                    else:
                        payload = {'mac_id': address.lower(), 'last_sent_dt': datetime.datetime.now()}
                        self.local_payload_cache[address.lower()] = payload                     
                        r = requests.get("http://127.0.0.1:8000/hummingbird/build_user_from_device/", params=payload)               
                        cached = False
                else:
                    payload = {'mac_id': address.lower(), 'last_sent_dt': datetime.datetime.now()}
                    r = requests.get("http://127.0.0.1:8000/hummingbird/build_user_from_device/", params=payload)               
                    cached = False

                ## Convert the string representation of a dicitonary with user info into a dictionary object.
                user_dict = ast.literal_eval(r.text)
                
                if not cached and user_dict!=0:
                    user = User(system=self, name=user_dict['name'], song=user_dict['song'], length=float(user_dict['length']), arrival=datetime.datetime.strptime(user_dict['last_played'],'%Y-%m-%d %H:%M:%S'))
                    # play the user's song (if theirs hasn't played already)
                    # if user.song != settings.DO_NOT_PLAY and user.has_not_played_today():
                    if user.has_not_played_today():
                        if not is_unknown_user(name=user.name) or config.play_unknowns:
                            log(message="Detected activity from {name}.".format(name=user.name))
                            user.queue_song(music_player=self.music_player)
                            updated = requests.get("http://127.0.0.1:8000/hummingbird/update_last_played/", params=payload)

    def input_timeout(self):
        if self.waiting_for_input:
            log(message="Warning: tcpdump has not provided input for a while. There may be something wrong.")
        else:
            self.waiting_for_input = True
            threading.Timer(interval=config.time_input_timeout, function=self.input_timeout).start()

    def add_new_address(self, address, user_name=config.unknown_user_prefix):
        # if the address is new, add it to our dict
        if address not in self.all_addresses:
            user = User(system=self, name=user_name)
            self.all_addresses[address] = user

            with open(config.data_file, 'a') as f:
                f.write("{address},{name},{song}\n".format(address=address, name=user.name, song=user.song))

            if is_unknown_user(name=user.name):
                log(message="A new unknown device with address {address} has been added and has been assigned {song}.".format(address=address, song=user.song))
            else:
                log(message="{name} has been added and has been assigned {song}.".format(name=user.name, song=user.song))

System()
