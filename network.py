import re

import config

def get_MAC(line):
	# check if line should be ignored
	for regex in config.tcpdump_re_ignore:
		if re.match(regex, line):
			return []

	# check for MAC addresses
	for val in config.tcpdump_re.itervalues():
		regex, groups = val
		regex_match = re.match(regex, line)
		if regex_match:
			addresses = [regex_match.group(x) for x in groups]
			# return all non-multicast addresses
			return [x for x in addresses if x[:8] != "01:00:5e" and x[:5] != "33:33"]
	
	# report unrecognized lines from tcpdump
	with open(config.tcpdump_did_not_match_log, 'a') as f:
		f.write(line)
	return []
