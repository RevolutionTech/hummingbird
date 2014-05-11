import string
import random

import config

def generate_random_suffix(length=config.unknown_user_suffix_length):
	chars_allowed = string.lowercase + string.uppercase + string.digits
	random_suffix = []
	for i in xrange(0, length):
		random_suffix.append(random.choice(chars_allowed))
	return ''.join(random_suffix)

def is_unknown_user(user_name):
	return len(user_name) >= len(config.unknown_user_prefix) and user_name[:len(config.unknown_user_prefix)] == config.unknown_user_prefix
