import re

import config

def get_MAC(line):
	addresses = []

	message_re = re.match(config.tcpdump_message_re, line)
	broadcast_re = re.match(config.tcpdump_broadcast_re, line)
	message_mac_re = re.match(config.tcpdump_message_mac_re, line)
	broadcast_mac_re = re.match(config.tcpdump_broadcast_mac_re, line)
	probe_request_mac_re = re.match(config.tcpdump_probe_request_mac_re, line)
	probe_response_mac_re = re.match(config.tcpdump_probe_response_mac_re, line)
	acknowledgement_mac_re = re.match(config.tcpdump_acknowledgement_mac_re, line)
	data_iv_mac_re = re.match(config.tcpdump_data_iv_mac_re, line)
	if message_re:
		addresses = [message_re.group(2), message_re.group(4)]
	elif broadcast_re:
		addresses = [broadcast_re.group(2)]
	elif message_mac_re:
		addresses = [message_mac_re.group(2), message_mac_re.group(4), message_mac_re.group(6)]
	elif broadcast_mac_re:
		addresses = [broadcast_mac_re.group(2), broadcast_mac_re.group(4)]
	elif probe_request_mac_re:
		addresses = [probe_request_mac_re.group(2)]
	elif probe_response_mac_re:
		addresses = [probe_response_mac_re.group(2), probe_response_mac_re.group(4), probe_response_mac_re.group(6)]
	elif acknowledgement_mac_re:
		addresses = [acknowledgement_mac_re.group(2)]
	elif data_iv_mac_re:
		addresses = [data_iv_mac_re.group(2), data_iv_mac_re.group(4), data_iv_mac_re.group(6)]
	elif line != '\n':
		with open("tcpdump_dnm.log", 'a') as f:
			f.write(line)

	# ignore multicast addresses
	return [x for x in addresses if x[:8] != "01:00:5e" and x[:5] != "33:33"]
