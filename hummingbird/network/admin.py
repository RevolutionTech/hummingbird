import re
import subprocess

import config
from utils import Log

class NetworkManager:
	def __init__(self, user_manager):
		self.user_manager = user_manager
		self.tcpdump_re_ignore = map(re.compile, config.tcpdump_re_ignore)
		self.tcpdump_re = dict(
			map(
				lambda (k, v): (k, (re.compile(v[0]), v[1])),
				config.tcpdump_re.iteritems()
			)
		)

	def init_network(self):
		Log.log(message="Initiating Network Manager...", locations=[Log.STDOUT,])
		popen = subprocess.Popen("./tcpdump", stdout=subprocess.PIPE)
		for line in iter(popen.stdout.readline, ""):
			# handle input as network traffic from tcpdump
			if config.tcpdump_to_stdout:
				print line
			addresses = self.get_MAC(line=line)
			for address in addresses:
				self.user_manager.MAC_detected(address=address)

	def get_MAC(self, line):
		# check if line should be ignored
		for regex in self.tcpdump_re_ignore:
			if re.match(regex, line):
				return []

		# check for MAC addresses
		for val in self.tcpdump_re.itervalues():
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
