import datetime

import config
from users.models import UserProfile

def log(message):
	print "[{timestamp}] {message}".format(timestamp=datetime.datetime.now().replace(microsecond=0), message=message)

def print_MAC_address(address):
	if config.print_all_MACs:
		try:
			userprofile = UserProfile.objects.get(mac_address=address)
			log(message="MAC detected: {address}; owned by {name}".format(address=address, name=userprofile.user.first_name))
		except UserProfile.DoesNotExist:
			log(message="MAC detected: {address}".format(address=address))

def create_kwargs(request, params):
		kwargs = {}
		for param in params:
			optional = True
			if len(param) == 2:
				name, _type = param
			else:
				name, _type, optional = param
			try:
				kwargs[name] = _type(request.GET[name])
			except KeyError:
				if not optional:
					raise AssertionError("Expected parameter {param}".format(param=name))
		return kwargs
