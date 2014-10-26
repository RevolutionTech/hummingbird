import subprocess

import config
from utils import Log

class NetworkManager:
	def __init__(self, user_manager):
		self.user_manager = user_manager

	@staticmethod
	def bpf_filter_from_ignored_hosts():
		return ' and '.join(map(lambda x: 'not ether host {}'.format(x), config.ignored_hosts))

	def init_network(self):
		Log.log(message="Initiating Network Manager...", locations=[Log.STDOUT,])
		popen = subprocess.Popen(
			["tshark", "-i", config.network_interface, self.bpf_filter_from_ignored_hosts(), "-e", "eth.src", "-Tfields"],
			stdout=subprocess.PIPE
		)
		for line in iter(popen.stdout.readline, ""):
			self.MAC_from_network(line.replace('\n', ''))

	def MAC_from_network(self, line):
		if config.network_dump_to_stdout:
			Log.log(message=line, locations=[Log.STDOUT,])
		if line.startswith('01:00:5e') or line.startswith('33:33'):
			return
		self.user_manager.MAC_detected(address=line)
