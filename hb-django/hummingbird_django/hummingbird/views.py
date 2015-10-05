from django.shortcuts import render
from hummingbird.models import UserProfile, UserDevice, User
from django.http import HttpResponse
import datetime
import urllib
# Create your views here.

#def index(request):
#    return HttpResponse("hummingbird index")


def index(request):
    userprofile_list = UserProfile.objects.order_by('-last_played')
    context_dict = {'userprofiles': userprofile_list}
    response = render(request, 'index.html',context_dict)
    return response

def profile(request, user_id):
	context_dict = {}
	try:
		userprofile = UserProfile.objects.get(pk=user_id)
		context_dict['name'] = userprofile.name
		if userprofile.song:
			context_dict['song'] = userprofile.song.name
		if userprofile.last_played:
			context_dict['last_played'] = userprofile.last_played.strftime('%Y-%m-%d %H:%M:%S')
		context_dict['length'] = userprofile.length
	except UserProfile.DoesNotExist:
		pass
	return render(request,'profile.html',context_dict)



def get_user_from_device(request):
	if request.method == 'GET':
		try:
			device = request.GET['mac_id']
			userdevice = UserDevice.objects.get(mac_id=device)
			user = userdevice.user_profile.user_id.id
			return HttpResponse(user, content_type='text/plain')
		except UserDevice.DoesNotExist:
			return HttpResponse("0", content_type='text/plain')
	pass

def build_user_from_device(request):
	if request.method == 'GET':
		try:
			device=urllib.unquote(request.GET['mac_id']).decode('utf8')
			print device
			userdevice = UserDevice.objects.get(mac_id=device)
			user = userdevice.user_profile.user_id.id
			user_dict={}
			user_dict['name'] = userdevice.user_profile.name
			user_dict['song'] = userdevice.user_profile.song.name
			user_dict['length'] = userdevice.user_profile.length
			user_dict['last_played'] = userdevice.user_profile.last_played.strftime('%Y-%m-%d %H:%M:%S')
			return HttpResponse(str(user_dict), content_type='text/plain')
	### TO DO: Create dictionary/list to return
		except UserDevice.DoesNotExist:
			return HttpResponse("0", content_type='text/plain')
	pass

def update_last_played(request):
	if request.method == 'GET':
		device=urllib.unquote(request.GET['mac_id']).decode('utf8')
		userdevice = UserDevice.objects.get(mac_id=device)
		userprofile = userdevice.user_profile
		userprofile.last_played = datetime.datetime.now()
		userprofile.save()
		return HttpResponse("Updated User", content_type='text/plain')
	else:
		return HttpResponse("0", content_type='text/plain')

def get_song_from_user(request):
	if request.method == 'GET':
		user_id = request.GET['user_id']
		user_profile = UserProfile.objects.get(pk=user_id)
		song = user_profile.song

def has_user_played_today(request):
	if request.method == 'GET':
		user_id = request.GET['user_id']
		user_profile = UserProfile.objects.get(pk=user_id)
		last_played = user_profile.last_played
		now = datetime.datetime.now()
		today = now.date()
		yesterday = today - datetime.timedelta(days=1)
		return (
			now.time() >= settings.TIME_RESET_TIME and self.arrival < datetime.datetime.combine(today, settings.TIME_RESET_TIME)
		) or (
			now.time() < settings.TIME_RESET_TIME and self.arrival < datetime.datetime.combine(yesterday, settings.TIME_RESET_TIME)
		)





def testuser(request):
	if request.method == 'GET':
		device = request.GET['mac_id']
		print device
		userdevice = UserDevice.objects.get(mac_id=device)
		print userdevice
		userprofile = userdevice.user_profile
		print userprofile
		song = userprofile.song
		print song
		return HttpResponse(userprofile, content_type='text/plain')
	return HttpResponse("2")


def about(request):
	pass