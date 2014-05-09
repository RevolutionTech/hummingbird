import re

import config

def get_MAC(line):
	addresses = []

	message_re = re.match(config.tcpdump_message_re, line)
	broadcast_re = re.match(config.tcpdump_broadcast_re, line)
	if message_re:
		addresses = [message_re.group(2), message_re.group(4)]
	elif broadcast_re:
		addresses = [broadcast_re.group(2)]
	elif line != '\n':
		with open("tcpdump_dnm.log", 'a') as f:
			f.write(line)

	# ignore multicast addresses
	return [x for x in addresses if x[:8] != "01:00:5e" and x[:5] != "33:33"]
