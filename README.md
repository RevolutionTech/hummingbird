# Hummingbird
# Walk-in songs
# Created by: Lucas Connors

You will need to enable promiscuous mode on the machine you are running Hummingbird on for it to read packets from other devices.

Then once you've done that, run Hummingbird by piping output from tcpdump using the following command:

`sudo tcpdump -e -i wlan0 2>> tcpdump_error.log | python hummingbird.py`

Dependencies:
- standard Python libraries (obviously)
- pygame
