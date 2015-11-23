# Hummingbird: Walk-in songs
# Created by: Lucas Connors

![Hummingbird](http://revolutiontech.bitbucket.org/img/code/hummingbird.png)

***

## About

Hummingbird is an application used to play custom theme songs (or walk-in songs) when a person enters a building. Hummingbird monitors the network and detects when a new device (identified by its MAC address) connects to the router. When a new device connects, Hummingbird plays the song associated with that device.

Hummingbird is a simple program designed to run continuously on a computer connected to speakers. A [Raspberry Pi](http://www.raspberrypi.org/) with a Wi-Fi dongle may prove to be a good setup for Hummingbird.

## Prerequisites

Hummingbird requires [pygame](http://www.pygame.org/download.shtml) for playing sound, which you can install on Debian with:

`sudo apt-get install python-pygame`

To use Hummingbird, you may need to [enable monitor mode](http://wiki.wireshark.org/CaptureSetup/WLAN#Turning_on_monitor_mode) (sometimes called promiscuous mode) on the network interface being used. This is so the program can read packets from other devices in order to detect when a new device is nearby.

## Configuration

Custom walk-in songs should be stored in the subdirectory `audio/`. Inside that directory, there should be another subdirectory `random/` where additional songs are included for the assignment of unknown MAC addresses (see below).

Associations are listed in a comma-separated value file called `songs.csv`. Each line should contain at least three items: MAC address, name, and path/to/song. Such a file may look like the following:

	aa:bb:cc:dd:ee:ff,John,audio/John.mp3
	00:11:22:33:44:55,John-MacBook,DNP
	bb:cc:dd:ee:ff:aa,Smith,NTA
	cc:dd:ee:ff:aa:bb,Mary,audio/Mary.mp3
	dd:ee:ff:aa:bb:cc,Brown,audio/Brown.mp3,24

A line may also have an optional fourth item which is interpreted as the length of time that the song should play for (in seconds). By default, each song plays for a maximum of 20 seconds and so this option allows for exceptions to that length. If `DNP` (Do Not Play) is provided for the path, then no song will play when the MAC address in that line is detected. This is useful for laptops and desktop computers. If `NTA` (Need To Assign) is provided for the path, then a song will be randomly chosen for this user (out of the songs under `audio/random/`) when Hummingbird starts.

Some configuration settings can be easily changed by modifying `config.py`. For example, by default unknown MAC addresses will not cause a song to play (to avoid strangers walking by from being observed by the system). However, Hummingbird can be easily changed so that new MAC addresses are automatically assigned a walk-in song from `audio/random/` on the first time that they connect.

## Running

Once Hummingbird has been configured, most users can then run Hummingbird with the following command:

`./go_hummingbird`

If you run into issues, it may either be because the network interface picked up by the script is wrong or the Python version used is incorrect. You can override the network interface used with `export INTERFACE=wlan0` where `wlan0` is the correct interface and you can override the Python version used with `export PYGAMEPYTHON=python2.7-32` where `python2.7-32` is the Python version with Pygame installed.

While Hummingbird is running, the network interface will be unable to connect to the router. This means that *you will not be able to connect to the Internet*. Once you are done using Hummingbird, you may have to turn your Wifi off and back on again to resume normal operation.

## Improve Hummingbird

Sometimes Hummingbird receives input from `tcpdump` that I did not anticipate. If this happens, the input will be ignored and it will not detect any MAC addresses (which might mean that devices go undetected). However, if input is not understood by Hummingbird it will automatically be dumped to a file called `tcpdump_dnm.log`.

If you notice `tcpdump_dnm.log` appear, please send it (or even just part of the file) to `lucas [at] revolutiontech [dot] ca` and I will try to fix the problem. Feel free to delete the file once you have reported the issue.

Any other bugs to report, suggestions for improvement, feature requests, government secrets, etc. please feel free to send my way. Contributions to the repo are especially welcome!
