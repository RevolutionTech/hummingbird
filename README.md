# Hummingbird: Walk-in songs
# Created by: Lucas Connors

![Hummingbird](http://revolutiontech.bitbucket.org/img/code/hummingbird.png)

***

## About

Hummingbird is a server used to play custom theme songs (or walk-in songs) when a person enters a building. Hummingbird monitors the network and detects when a new device (identified by its MAC address) connects to the router. When a new device connects, Hummingbird plays the song associated with that device.

Hummingbird is designed to run continuously on a server connected to speakers and Wi-Fi. A [Raspberry Pi](http://www.raspberrypi.org/) with a Wi-Fi dongle may prove to be a good setup for Hummingbird.

## Prerequisites

Hummingbird requires [MySQL](http://www.mysql.com/), which you can install on debian with:

`sudo apt-get install mysql-server mysql-client`

Once you have installed mysql, you should create a database for Hummingbird and then store the user credentials to the database (`DATABASE_USER` and `DATABASE_PASSWORD`) in a file called `hummingbird/settings/settings_secret.py`.

I recommend using a virtual environment for Hummingbird. If you don't have it already, you can install [virtualenv](http://virtualenv.readthedocs.org/en/latest/virtualenv.html) globally with pip:

`sudo pip install virtualenv`

Then in your virtual environment, you will need to install [pygame](http://www.pygame.org/wiki/about), [django](https://www.djangoproject.com/), and [south](http://south.readthedocs.org/en/latest/installation.html):

`sudo apt-get install python-pygame`

`pip install django`

`pip install south`

With everything installed, you will then have to create the database tables, which you can do with:

`./manage.py migrate`

To use Hummingbird, you may need to [enable monitor mode](http://wiki.wireshark.org/CaptureSetup/WLAN#Turning_on_monitor_mode) (sometimes called promiscuous mode) on the network interface being used by the server. This is so Hummingbird can read packets from other devices in order to detect when a new device is nearby.

## Configuration

Custom walk-in songs should be stored in the subdirectory `audio/`. Inside that directory, there should be another subdirectory `random/` where additional songs are included for users that do not provide a walk-in song.

The server can be run on port 8000 with `./manage.py runserver 0.0.0.0:8000`. Then the server can be reached from the browser at `http://0.0.0.0:8000/`.

You can create a user for Joe and assign him the walk-in song `audio/joe.mp3` by hitting the URL: `/users/create_user?email=jsmith@email.com&mac_address=aa:bb:cc:dd:ee:ff&first_name=Joe&song_title=joe.mp3`. Additional parameters are available, such as the delay before the walkin-song plays, the length of the walk-in song, and artist and album of the walk-in song, and more.

If `song_title` is not specified, the user created will be assigned a random song (which will cause an exception if there are no random songs in Hummingbird).

Changing values in the database requires accessing the shell via `./manage.py shell`. You must also access the shell to add new songs for users or random songs initially unassigned to any users.

Additional configuration is available by modifying the `config.py` file.

## Running

Once Hummingbird has been configured and the server is running, then the network manager and media player can be activated by hitting the URL: `/init_hummingbird`. This will generate a persistent instance of the network manager and media player, so you will not want to do this multiple times while the server is running.

The server will then make a `sudo` call to `tcpdump`, so the server will then be hanging waiting for you to type in the password for sudo in the terminal window that you ran `runserver` in.

Note that while Hummingbird is running, the network interface may be unable to connect to the router. This could mean that *you will not be able to connect to the Internet*. Once you are done using Hummingbird, you may have to turn your Wifi off and back on again to resume normal operation.

## Improve Hummingbird

Sometimes Hummingbird receives input from `tcpdump` that I did not anticipate. If this happens, the input will be ignored and it will not detect any MAC addresses (which might mean that devices go undetected). However, if input is not understood by Hummingbird it will automatically be dumped to a file called `tcpdump_dnm.log`.

If you notice `tcpdump_dnm.log` appear, please send it (or even just part of the file) to `lucas [at] revolutiontech [dot] ca` and I will try to fix the problem. Feel free to delete the file once you have reported the issue.

Any other bugs to report, suggestions for improvement, feature requests, government secrets, etc. please feel free to send my way. Contributions to the repo are especially welcome!
