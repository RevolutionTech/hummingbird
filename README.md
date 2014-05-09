# Hummingbird: Walk-in songs
# Created by: Lucas Connors

***

## About

Hummingbird is an application used to play custom theme songs (or walk-in songs) when a person enters a building. Hummingbird monitors the network and detects when a new device (identified by its MAC address) connects to the router. When a new device connects, Hummingbird plays the song associated with that device.

Hummingbird is a simple program designed to run continuously on a computer connected to speakers. A [Raspberry Pi](http://www.raspberrypi.org/) with a Wi-Fi dongle may prove to be a good setup for Hummingbird.

## Prerequisites

Hummingbird requires [pygame](http://www.pygame.org/download.shtml) for playing sound, which you can install on Debian with:

`sudo apt-get install python-pygame`

To use Hummingbird, you will need to [enable monitor mode](http://wiki.wireshark.org/CaptureSetup/WLAN#Turning_on_monitor_mode) (sometimes called promiscuous mode) on the network interface that is connected to the main router being used. This is so the program can read packets from other devices in order to detect when a new device connects to the router.

## Configuration

Custom walk-in songs should be stored in the subdirectory `audio/bytes/`. Inside that directory, there should be another subdirectory `random/` where additional songs are included for the assignment of unknown MAC addresses (see below).

Associations are listed in a comma-separated value file called `songs.csv`. Each line should contain three items: MAC address, name, and path/to/song. Such a file may look like the following:

	aa:bb:cc:dd:ee:ff,John,audio/bytes/John.mp3
	bb:cc:dd:ee:ff:aa,Smith,audio/bytes/Smith.mp3
	cc:dd:ee:ff:aa:bb,Mary,audio/bytes/Mary.mp3
	dd:ee:ff:aa:bb:cc,Brown,audio/bytes/Brown.mp3

Some configuration settings can be easily changed by modifying `config.py`. For example, by default unknown MAC addresses will not cause a song to play (to avoid strangers walking by from observed the system). However, Hummingbird can be easily changed so that new MAC addresses are automatically assigned a walk-in song from `audio/bytes/random/` on the first time that they connect.

Once Hummingbird has been configured, you can run Hummingbird by piping output from tcpdump using the following command:

`sudo tcpdump -e -i wlan0 2>> tcpdump_error.log | python hummingbird.py`

Please note that you may need to replace `wlan0` with a different interface, depending on which one is connected to the router.