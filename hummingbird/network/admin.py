import re
import subprocess

import config
from utils import Log

class NetworkManager:
	def __init__(self, user_manager):
		self.user_manager = user_manager
		self.mac_address_re = re.compile(config.mac_address_re)

	def init_network(self):
		Log.log(message="Initiating Network Manager...", locations=[Log.STDOUT,])
		popen = subprocess.Popen("./tcpdump", stdout=subprocess.PIPE)
		for line in iter(popen.stdout.readline, ""):
			line = line.replace('\n', '')
			# handle input as network traffic from tcpdump
			if config.tcpdump_to_stdout:
				print line
			address = self.get_MAC(line=line)
			if address:
				self.user_manager.MAC_detected(address=address)

	def get_MAC(self, line):
		# check for MAC address
		if re.match(self.mac_address_re, line) and \
			line[:8] != "01:00:5e" and line[:5] != "33:33":
			return line
