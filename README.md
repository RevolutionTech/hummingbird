# Hummingbird
# Walk-in songs
# Created by: Lucas Connors

Run Hummingbird by piping output from tcpdump using the following command:

`sudo tcpdump -e -i wlan0 2>> tcpdump_error.log | python hummingbird.py`