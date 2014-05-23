import datetime

# Main Settings
play_unknowns = False

# Time Settings
time_reset_time = datetime.time(hour=4, minute=0) # 4:00am
time_wait_to_play = 60 * 5 # 5 minutes
time_delay_to_play_song = 15
time_check_queue = 0.25
time_input_timeout = 30
time_max_song_length = 20
time_fadeout_song = 3000 # in milliseconds

# User Files
data_file = "songs.csv"
audio_dir = "audio/"
random_subdir = "random/"
tcpdump_did_not_match_log = "tcpdump_dnm.log"

# Data Settings
do_not_play = "DNP"
need_to_assign = "NTA"
unknown_user_prefix = "Unknown #"
unknown_user_suffix_length = 5

# Network
tcpdump_re_ignore = [
	"^$",
	"^(\d{2}:){2}\d{2}.\d+ \[\|802.11\]$",
	"^(\d{2}:){2}\d{2}.\d+ \d+us tsft short preamble \d+\.?\d? Mb/s \d+ MHz \(0x\d+\) -?\d+dB signal -?\d+dB noise antenna 0 \(H\) Unknown Ctrl SubtypeUnknown Ctrl Subtype$"
]
tcpdump_re = {
	# format: key (string) to tuple of regex (string) and list of groups to match (ints)
	'regular_message': ("^(\d{2}:){2}\d{2}.\d+ (([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}) .*> (([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}) .*, .*$", [2, 4]),
	'regular_broadcast': ("^(\d{2}:){2}\d{2}.\d+ (([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}) .*> Broadcast, .*$", [2]),
	'message': ("^(\d{2}:){2}\d{2}.\d+ .* BSSID:(([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}) .* DA:(([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}) .* SA:(([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}) .*$", [2, 4, 6]),
	'broadcast': ("^(\d{2}:){2}\d{2}.\d+ \d+.* BSSID:(([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}) .* DA:Broadcast SA:(([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}) .*$", [2, 4]),
	'probe_request': ("^((\d{2}:){2}\d{2}.\d+ .* BSSID:Broadcast DA:Broadcast SA:(([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2})) .*$", [3]),
	'probe_response': ("^(\d{2}:){2}\d{2}.\d+ .* BSSID:(([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}) .* DA:(([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}) .* SA:(([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}) .*$", [2, 4, 6]),
	'acknowledgement': ("^(\d{2}:){2}\d{2}.\d+ .* RA:(([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}) .*$", [2]),
	'data_iv_message': ("^(\d{2}:){2}\d{2}.\d+ .* DA:(([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}) .* BSSID:(([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}) .* SA:(([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}) .*$", [2, 4, 6]),
	'data_iv_broadcast': ("^(\d{2}:){2}\d{2}.\d+ .* BSSID:(([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}) .* SA:(([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}) .*$", [2, 4]),
	'power_save_poll': ("^(\d{2}:){2}\d{2}.\d+ .* BSSID:(([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}) .* TA:(([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}) .*$", [2, 4]),
	'noise_antenna': ("^(\d{2}:){2}\d{2}.\d+ .* RA:Broadcast BSSID:(([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}) .*$", [2])
}

# Debugging
wait_to_play = True
print_all_MACs = False
