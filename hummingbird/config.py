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
time_fadeout_song = 1000 * 3 # 3 seconds

# Log Settings
activity_events_per_page = 15
network_dump_to_stdout = True
verbose_logging_to_stdout = True

# Data Settings
user_password_min_length = 5
song_title_max_length = 35
song_artist_max_length = 20
song_album_max_length = 20

# Network
network_interface = 'wlan0'
with open('ignored_hosts') as f:
	ignored_hosts = filter(lambda x: x, map(lambda x: x.strip('\n'), f.readlines()))
