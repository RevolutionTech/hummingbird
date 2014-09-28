# Hummingbird: Walk-in songs
# Created by: Lucas Connors

![Hummingbird](http://revolutiontech.ca/img/code/hummingbird.png)

***

## About

Hummingbird is a server used to play custom theme songs (or walk-in songs) when a person enters a building. Hummingbird monitors the network and detects when a new device (identified by its MAC address) connects to the router. When a new device connects, Hummingbird plays the song associated with that device.

Hummingbird is designed to run continuously on a server connected to speakers and Wi-Fi. A [Raspberry Pi](http://www.raspberrypi.org/) with a Wi-Fi dongle may prove to be a good setup for Hummingbird.

Hummingbird is under active development. Follow my progress [on Trello](https://trello.com/b/DK5BO6ev/hummingbird).

## Setup

**Note: This portion of this README assumes the reader has some basic knowledge of Django.**

### Prerequisites

To use Hummingbird, you may need to [enable monitor mode](http://wiki.wireshark.org/CaptureSetup/WLAN#Turning_on_monitor_mode) (sometimes called promiscuous mode) on the network interface being used by the server. This is so Hummingbird can read packets from other devices in order to detect when a new device is nearby.

Additionally, Hummingbird requires [MySQL](http://www.mysql.com/), which you can install on debian with:

    sudo apt-get -y install mysql-server mysql-client libmysqlclient-dev

Remember the database credentials, because we will need them later in the setup.

I recommend using a virtual environment for Hummingbird. If you don't have it already, you can install [virtualenv](http://virtualenv.readthedocs.org/en/latest/virtualenv.html) and virtualenvwrapper globally with pip:

    sudo pip install virtualenv virtualenvwrapper

[Update your .profile or .bashrc file](http://virtualenvwrapper.readthedocs.org/en/latest/install.html#shell-startup-file) to create new environment variables for virtualenvwrapper and then create and activate your virtual environment with:

    mkvirtualenv hummingbird

In the future you can reactivate the virtual environment with:

    workon hummingbird

### Installation

Then in your virtual environment, you will need to install [pygame](http://www.pygame.org/wiki/about), MySQL-python, [django](https://www.djangoproject.com/), and [south](http://south.readthedocs.org/en/latest/installation.html):

    sudo apt-get -y install libsox-fmt-mp3 libsox-fmt-all mpg321 dir2ogg libav-tools
    sudo apt-get -y build-dep python-pygame
    yes y | pip install git+http://github.com/xamox/pygame
    pip install MySQL-python django south

### Configuration

Next we will need to create a file in the same directory as `settings.py` called `settings_secret.py`. This is where we will store all of the settings that are specific to your instance of Hummingbird. Most of these settings should be only known to you. Your file should define a secret key, the database credentials, and an email where you (as an administrator of the Hummingbird instance) can be reached. Your `settings_secret.py` file might look something like:

    SECRET_KEY = '-3f5yh&(s5%9uigtx^yn=t_woj0@90__fr!t2b*96f5xoyzb%b'
    DATABASE_USER = 'root'
    DATABASE_PASSWORD = 'abc123'
    FEEDBACK_EMAIL = 'admin+hummingbird@company.com'

Of course you should [generate your own secret key](http://stackoverflow.com/a/16630719) and use a more secure password for your database.

Additional configuration is available by modifying the `config.py` file.

With everything installed and all files in place, you may now create the database tables. You can do this with:

    python manage.py syncdb
    python manage.py migrate

### Running

The server can be run on port 8000 with `python manage.py runserver 0.0.0.0:8000`. Then the server can be reached from the browser at `http://0.0.0.0:8000/`.

Hitting that URL should reach the user interface where users can create accounts, upload new songs, and modify their profile information.

Once Hummingbird has been configured and the server is running, then the network manager and media player can be activated by running the `init_hummingbird()` function from the shell:

    python manage.py shell
    >>> from users.admin import UserManager
    >>> um = UserManager()
    >>> um.init_hummingbird()

This will generate a persistent instance of the network manager and media player, so you will not want to do this multiple times while the server is running.

The server will then make a `sudo` call to `tcpdump`, so you will need to type in the password for sudo.

Note that while Hummingbird is running, the network interface may be unable to connect to the router. This could mean that *you will not be able to connect to the Internet*. Once you are done using Hummingbird, you may have to turn your Wifi off and back on again to resume normal operation.

## Improve Hummingbird

Any other bugs to report, suggestions for improvement, feature requests, government secrets, etc. please feel free to send my way. Contributions to the repo are especially welcome!
