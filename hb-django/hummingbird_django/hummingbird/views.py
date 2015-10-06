from django.shortcuts import render
from hummingbird.models import UserProfile, UserDevice, User
from hummingbird.forms import UserProfileForm, UserDeviceForm, UserSongForm
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
	added_song=False
	added_device=False
	context_dict = {}

	if request.method == 'POST':
		userprofile = UserProfile.objects.get(pk=user_id)
		usersong_form = UserSongForm(data=request.POST)
		device_form = UserDeviceForm(data=request.POST)
	
		if usersong_form.is_valid():
			userprofile.song = request.FILES['song']
			userprofile.save()
			added_song = True
	
		if device_form.is_valid():
			device = device_form.save(commit=False)
			device.user_profile = userprofile
			added_device = True
			device.save()
	
	try:
		userprofile = UserProfile.objects.get(pk=user_id)
		context_dict['profile'] = userprofile
		context_dict['name'] = userprofile.name
		if userprofile.song:
			context_dict['song'] = userprofile.song.name
		if userprofile.last_played:
			context_dict['last_played'] = userprofile.last_played.strftime('%Y-%m-%d %H:%M:%S')
		context_dict['length'] = userprofile.length
		
		devices = UserDevice.objects.filter(user_profile=userprofile)
		context_dict['devices'] = devices
		usersong_form = UserSongForm()
		device_form = UserDeviceForm()
		context_dict['usersong_form'] = usersong_form
		context_dict['device_form'] = device_form
	except UserProfile.DoesNotExist:
		pass
	context_dict['added_device'] = added_device
	context_dict['added_song'] = added_song
	return render(request,'profile.html',context_dict)



def get_user_from_device(request):
	if request.method == 'GET':
		try:
			device = request.GET['mac_id']
			userdevice = UserDevice.objects.get(mac_id=device)
			user = userdevice.user_profile.id
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


def add_user(request):
	registered = False
	if request.method == 'POST':
		profile_form = UserProfileForm(data=request.POST)
		device_form = UserDeviceForm(data=request.POST)
		if profile_form.is_valid():
			userprofile = profile_form.save()
			if 'song' in request.FILES:
				userprofile.song = request.FILES['song']
			userprofile.save()
			if device_form.is_valid():
				device_form.user_profile = userprofile
				device_form.save()

			registered = True
	else:
		profile_form = UserProfileForm()
		device_form = UserDeviceForm()

	return render(request,'add_user.html', {'profile_form':profile_form, 'device_form':device_form, 'registered':registered})

def delete_device(request):
	device_id = request.GET['device_id']
	device = UserDevice.objects.get(pk=device_id)
	device.delete()
	user_id = request.GET['user_id']
	devices = UserDevice.objects.filter(user_profile=user_id)
	return render(request, 'devices.html', {'devices':devices})

def delete_user(request):
	user_id = request.GET['user_id']
	userprofile=UserProfile.objects.get(pk=user_id)
	print userprofile
	devices = UserDevice.objects.filter(user_profile=userprofile)
	print devices
	for device in devices:
		print device
		device.delete()
	userprofile.delete()
	users = UserProfile.objects.all()
	return render(request, 'users.html', {'userprofiles':users})


def about(request):
	pass