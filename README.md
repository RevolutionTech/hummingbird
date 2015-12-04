# Hummingbird: Walk In With Style
# Created by: Lucas Connors & Ittai Barzilay

![Hummingbird](http://revolutiontech.ca/media/img/hummingbird-large.jpg)

***

## About

Hummingbird is a server used to play custom theme songs (or walk-in songs) when a person enters a building. Hummingbird monitors the network and detects when a new device (identified by its MAC address) connects to the router. When a new device connects, Hummingbird plays the song associated with that device.

Hummingbird has two components: the Django server and the Hummingbird daemon. The server is the interface for adding users, device MAC addresses, and songs. The daemon runs in the background sniffing for MAC addresses, and then fires off a local request to the Django server to see if a song should be played, and if so, which one.

Hummingbird is under active development. Follow our progress [on Trello](https://trello.com/b/DK5BO6ev/hummingbird).

## Setup

**Note: This portion of this README assumes the reader has some basic knowledge of Django.**

### Prerequisites

To use Hummingbird, you may need to [enable monitor mode](http://wiki.wireshark.org/CaptureSetup/WLAN#Turning_on_monitor_mode) (sometimes called promiscuous mode) on the network interface being used by the server. This is so Hummingbird can read packets from other devices in order to detect when a new device is nearby. Hummingbird currently uses TCPDump, but we will probably switch to tshark at some point. 

I recommend using a virtual environment for Hummingbird. If you don't have it already, you can install [virtualenv](http://virtualenv.readthedocs.org/en/latest/virtualenv.html) and virtualenvwrapper globally with pip:

    sudo pip install virtualenv virtualenvwrapper

[Update your .profile or .bashrc file](http://virtualenvwrapper.readthedocs.org/en/latest/install.html#shell-startup-file) to create new environment variables for virtualenvwrapper and then create and activate your virtual environment with:

    mkvirtualenv hummingbird

In the future you can reactivate the virtual environment with:

    workon hummingbird


One thing to note is that sometimes virtual environments have issues getting access to network-level activity, which Hummingbird needs to sniff out the MAC addresses.

### Installation

Then in your virtual environment, you will need to install [pygame](http://www.pygame.org/wiki/about), MySQL-python, [django](https://www.djangoproject.com/), and [pydub](http://pydub.com/):

    sudo apt-get -y install libsox-fmt-mp3 libsox-fmt-all mpg321 dir2ogg libav-tools
    sudo apt-get -y build-dep python-pygame
    yes y | pip install -r requirements.txt

### Configuration

You should [generate your own secret key](http://stackoverflow.com/a/16630719) for the settings.py file.

Additional configuration is available by modifying the `config.py` file.

With everything installed and all files in place, you may now create the database tables. You can do this with:

    python manage.py syncdb
    python manage.py migrate

You will also need to create a superuser for Admin use, which you can do with
    
    python manage.py createsuperuser

### Running

1) The Django Server
The server can be run on port 8000 with `python manage.py runserver 0.0.0.0:8000`. Then the server can be reached from the browser at `http://0.0.0.0:8000/`. Specifying "0.0.0.0" allows external computers to access the server on port 8000 of the device running the server. So if the local IP address for the computer was 10.0.0.1, then any computer on the same network should be able to access hummingbird by navigating to 10.0.0.1:8000.

Hitting that URL should reach the user interface where users can create accounts, upload new songs, and modify their profile information.

2) The Hummingbird Daemon
Once the Django server has been configured and is running, then the network manager and media player can be initialized. This will generate a persistent instance of the network manager and media player, so you will not want to do this multiple times while the server is running. You can fire this off by running the command:

	./go_hummingbird

Note that while Hummingbird is running, the network interface may be unable to connect to the router. This could mean that *you will not be able to connect to the Internet*. Once you are done using Hummingbird, you may have to turn your Wifi off and back on again to resume normal operation.

## Improve Hummingbird


Any bugs to report, suggestions for improvement, feature requests, etc. please feel free to send our way. Contributions to the repo are especially welcome!
