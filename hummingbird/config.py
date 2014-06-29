import datetime

# Startup Settings
clear_queue = True
all_users_no_activity_today = False
wait_to_play = True

# Time Settings
time_reset_time = datetime.time(hour=4, minute=0) # 4:00am
time_wait_to_play = 60 * 5 # 5 minutes
time_check_queue = 0.25
time_input_timeout = 30
time_default_delay_to_play_song = 15
time_default_max_song_length = 20
time_fadeout_song = 3000 # in milliseconds

# User Files
tcpdump_did_not_match_log = "tcpdump_dnm.log"

# Log Settings
activity_events_per_page = 15
log_mac_addresses = False

# Data Settings
user_password_min_length = 5
song_title_max_length = 35
song_artist_max_length = 20
song_album_max_length = 20

# Network
tcpdump_re_ignore = [
	"^$",
	"^(\d{2}:){2}\d{2}.\d+ \[\|802.11\]$",
	"^(\d{2}:){2}\d{2}.\d+ \d+us tsft (short preamble )?\d+\.?\d? Mb/s \d+ MHz \(0x\d+\) -?\d+dB signal -?\d+dB noise antenna 0 \(H\) Unknown Ctrl SubtypeUnknown Ctrl Subtype$"
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
