import datetime

import config
from network.models import ActivityLog

class Log:

    STDOUT = 0
    DB = 1
    FILE = 2

    @classmethod
    def log(cls, message, locations=[DB,]):
        for location in locations:
            if location == cls.STDOUT and config.verbose_logging_to_stdout:
                print message
            elif location == cls.DB:
                ActivityLog.objects.create(message=message)

    @classmethod
    def log_MAC_address(cls, address):
        cls.log(
            message="MAC detected: {address}".format(address=address),
            locations=[cls.STDOUT,]
        )

def create_kwargs(request, params):
        kwargs = {}
        for param in params:
            optional = True
            if len(param) == 2:
                name, _type = param
            else:
                name, _type, optional = param
            if name in request.POST:
                kwargs[name] = _type(request.POST[name])
            elif name in request.GET:
                kwargs[name] = _type(request.GET[name])
            elif not optional:
                raise AssertionError("Expected parameter {param}".format(param=name))
        return kwargs

def has_not_played_today(dt):
    # not played today if:
    #   1) it's now after reset point and last played earlier today before reset point or earlier
    #   2) it's now before reset point and last played earlier yesterday before reset point or earlier
    now = datetime.datetime.now()
    today = datetime.datetime.combine(now.date(), config.time_reset_time)
    yesterday = today - datetime.timedelta(days=1)

    return (now.time() >= config.time_reset_time and dt < today) or \
        (now.time() < config.time_reset_time and dt < yesterday)
