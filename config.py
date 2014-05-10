tcpdump_message_re = "^(\d{2}:){2}\d{2}.\d+ (([0-9a-z]{2}:){5}[0-9a-z]{2}) [0-9a-zA-Z\(\) ]*> (([0-9a-z]{2}:){5}[0-9a-z]{2}) [0-9a-zA-Z\(\) ]*, .*$"
tcpdump_broadcast_re = "^(\d{2}:){2}\d{2}.\d+ (([0-9a-z]{2}:){5}[0-9a-z]{2}) [0-9a-zA-Z\(\) ]*> Broadcast, .*$"
tcpdump_message_mac_re = "^(\d{2}:){2}\d{2}.\d+ .* BSSID:(([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}) .* DA:(([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}) .* SA:(([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}) .*$"
tcpdump_broadcast_mac_re = "^(\d{2}:){2}\d{2}.\d+ \d+.* BSSID:(([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}) .* DA:Broadcast SA:(([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}) .*$"
tcpdump_probe_request_mac_re = "^((\d{2}:){2}\d{2}.\d+ .* BSSID:Broadcast DA:Broadcast SA:(([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2})) .*$"
tcpdump_probe_response_mac_re = "^(\d{2}:){2}\d{2}.\d+ .* BSSID:(([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}) .* DA:(([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}) .* SA:(([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}) .*$"
tcpdump_acknowledgment_mac_re = "^(\d{2}:){2}\d{2}.\d+ .* RA:(([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}) .*$"
tcpdump_data_iv_mac_re = "^(\d{2}:){2}\d{2}.\d+ .* DA:(([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}) .* BSSID:(([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}) .* SA:(([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}) .*$"

data_file = "songs.csv"
audio_bytes_dir = "audio/bytes/"
random_subdir = "random/"

do_not_play = "DNP"
need_to_assign = "NTA"
unknown_user_prefix = "Unknown #"
unknown_user_suffix_length = 5
play_unknowns = False

time_reset_system = 3600 * 24 # 1 day
time_wait_to_play = 60 * 6 # 6 minutes
time_check_queue = 0.25
time_max_song_length = 24
time_fadeout_song = 3000 # in milliseconds