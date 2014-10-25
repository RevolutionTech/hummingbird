import pyshark

import config
from utils import Log

class NetworkManager:
	def __init__(self, user_manager):
		self.user_manager = user_manager

	@staticmethod
	def ignored_hosts_lst_to_str(lst):
		return ' and '.join(map(lambda x: 'not ether host {}'.format(x), lst))

	def init_network(self):
		Log.log(message="Initiating Network Manager...", locations=[Log.STDOUT,])
		bpf_filter = self.ignored_hosts_lst_to_str(config.ignored_hosts)
		capture = pyshark.LiveCapture(interface='any', bpf_filter=bpf_filter)
		for packet in capture.sniff_continuously():
			if config.network_dump_to_stdout:
				Log.log(mesage=packet, locations=[Log.STDOUT,])
			address = packet.sll.src_eth
			self.user_manager.MAC_detected(address=address)
