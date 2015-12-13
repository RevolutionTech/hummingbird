import datetime
import string
import random

import config

def log(message):
	print "[{timestamp}] {message}".format(timestamp=datetime.datetime.now().replace(microsecond=0), message=message)

def generate_random_suffix(length=config.unknown_user_suffix_length):
	chars_allowed = string.lowercase + string.uppercase + string.digits
	random_suffix = []
	for i in xrange(0, length):
		random_suffix.append(random.choice(chars_allowed))
	return ''.join(random_suffix)

def is_unknown_user(name):
	return len(name) >= len(config.unknown_user_prefix) and name[:len(config.unknown_user_prefix)] == config.unknown_user_prefix