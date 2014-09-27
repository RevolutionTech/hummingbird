import datetime

from users.models import UserProfile
from network.models import ActivityLog

class Log:

	STDOUT = 0
	DB = 1
	FILE = 2

	@classmethod
	def log(cls, message, location=DB):
		if location == cls.DB:
			ActivityLog.objects.create(message=message)

	@classmethod
	def log_MAC_address(cls, address):
		try:
			userprofile = UserProfile.objects.get(mac_address=address)
			log(
				message="MAC detected: {address}; owned by {name}".format(
					address=address,
					name=userprofile.user.username
				),
				location=cls.STDOUT
			)
		except UserProfile.DoesNotExist:
			log(
				message="MAC detected: {address}".format(address=address),
				location=cls.STDOUT
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
