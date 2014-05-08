import re

import config

def get_MAC(line):
	message_re = re.match(config.tcpdump_message_re, line)
	broadcast_re = re.match(config.tcpdump_broadcast_re, line)
	if message_re:
		return [message_re.group(2), message_re.group(4)]
	elif broadcast_re:
		return [broadcast_re.group(2)]
	elif line != '\n':
		with open("tcpdump_dnm.log", 'a') as f:
			f.write(line)
	return []