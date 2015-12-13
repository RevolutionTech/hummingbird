import json
from django.shortcuts import render
from models import UserProfile, UserDevice, User
from forms import UserProfileForm, UserDeviceForm, UserSongForm
from django.http import HttpResponse
import datetime
import urllib


## TO-DO: Add div and context for files in library to allow for file deletion. As of right now, files will just accumulate in the library.
def index(request):
    userprofile_list = UserProfile.objects.order_by('-last_played')
    context_dict = {'userprofiles': userprofile_list}
    return render(request, 'index.html', context_dict)


## Returns info for userprofile page, and will update userprofile/userdevice fields if POST is used.
def profile(request, user_id):
    added_song=False
    added_device=False
    context_dict = {}

    ## If we're getting data via post method, update whatever fields we've been given.
    if request.method == 'POST':
        userprofile = UserProfile.objects.get(pk=user_id)
        usersong_form = UserSongForm(data=request.POST)
        device_form = UserDeviceForm(data=request.POST)
    
        if usersong_form.is_valid():
            userprofile.song = request.FILES['song']
            userprofile.length = usersong_form.cleaned_data['length']
            userprofile.save()
            added_song = True
    
        if device_form.is_valid():
            device = device_form.save(commit=False)
            device.user_profile = userprofile
            added_device = True
            device.save()
    
    ## Regardless of method (GET/POST), let's return info for the user's profile.
    try:
        userprofile = UserProfile.objects.get(pk=user_id)
    except UserProfile.DoesNotExist:
        pass
    else:
        context_dict['profile'] = userprofile
        context_dict['name'] = userprofile.name
        # If user has no song, the template will put in appropriate copy.
        if userprofile.song:
            context_dict['song'] = userprofile.song.name
        # If the user hasn't been played yet, the template will put in appropriate copy.
        if userprofile.last_played:
            context_dict['last_played'] = userprofile.last_played.strftime('%Y-%m-%d %H:%M:%S')     
        context_dict['length'] = userprofile.length
        # Add in devices to list for user's profile
        devices = UserDevice.objects.filter(user_profile=userprofile)
        context_dict['devices'] = devices
        # Populate forms
        usersong_form = UserSongForm()
        device_form = UserDeviceForm()
        context_dict['usersong_form'] = usersong_form
        context_dict['device_form'] = device_form
    # If we updated one of the fields, pass that to the template so it can tell the user that update was successful.
    context_dict['added_device'] = added_device
    context_dict['added_song'] = added_song
    return render(request, 'profile.html', context_dict)


## Checks if user exists. If so, return user name. Otherwise, return "0". 
def get_user_from_device(request):
    try:
        device = request.GET['mac_id']
        userdevice = UserDevice.objects.get(mac_id=device.lower())
        user = userdevice.user_profile.id
        return HttpResponse(user, content_type='text/plain')
    except UserDevice.DoesNotExist:
        return HttpResponse("0", content_type='text/plain')



## Returns information necessary to build the User object if mac_id is recognized. If not, return "0".
## If there is a user, a string representation of a dictioanry is returned.
def build_user_from_device(request):
    if request.method == 'GET':
        try:
            device = urllib.unquote(request.GET['mac_id']).decode('utf8')
            userdevice = UserDevice.objects.get(mac_id=device.lower()) 
            user_dict = {}
            user_dict['name'] = userdevice.user_profile.name
            # If user exists, but there is no song currently associated with them, we don't have anything to play,
            # so we return "0"
            if userdevice.user_profile.song.name == '':
                return HttpResponse("0", content_type='text/plain') 
            else:
                user_dict['song'] = userdevice.user_profile.song.name
            user_dict['length'] = userdevice.user_profile.length
            # Handle first-seen case. This will likely happen right after the device is added.
            # So, to prevent immediate playback after adding a user and device, if this is the 
            # first time a user is seen, just set the "last_played" field to now, and they will play tomorrow.
            if userdevice.user_profile.last_played is not None:
                user_dict['last_played'] = userdevice.user_profile.last_played.strftime('%Y-%m-%d %H:%M:%S')
            else: user_dict['last_played'] = datetime.datetime(1991, 1, 1).strftime('%Y-%m-%d %H:%M:%S')
            #return HttpResponse(str(user_dict), content_type='text/plain')
            return HttpResponse(json.dumps(user_dict), content_type='application/json')
        except UserDevice.DoesNotExist:
            return HttpResponse("0", content_type='text/plain')
    pass


## Once a user's song is played, Hummingbird uses this to update their "last_played" field to the current datetime.
def update_last_played(request):
    if request.method == 'GET':
        device = urllib.unquote(request.GET['mac_id']).decode('utf8')
        userdevice = UserDevice.objects.get(mac_id=device)
        userprofile = userdevice.user_profile
        userprofile.last_played = datetime.datetime.now()
        userprofile.save()
        return HttpResponse("Updated User", content_type='text/plain')
    else:
        return HttpResponse("0", content_type='text/plain')


## Right now, the actual "has played today" logic is being done in hummingbird.py.
## Eventually, we should move as much logic to the server sas possible. So, when
## we decide to do that, this function exists... but it's missing a return statement.
## So it may not do much right now.
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
    ## TODO: Figure out exactly how we want to migrate the logic to the server.

def add_user(request):
    registered = False
    if request.method == 'POST':
        profile_form = UserProfileForm(data=request.POST)
        device_form = UserDeviceForm(data=request.POST)
        if profile_form.is_valid():
            userprofile = profile_form.save()
            userprofile.last_played = datetime.datetime.now()
            if 'song' in request.FILES:
                userprofile.song = request.FILES['song']
            userprofile.save()
            if device_form.is_valid():
                deviceform = device_form.save()
                deviceform.user_profile = userprofile
                deviceform.save()
            registered = True
    else:
        profile_form = UserProfileForm()
        device_form = UserDeviceForm()

    return render(request, 'add_user.html', {'profile_form': profile_form, 'device_form': device_form, 'registered': registered})


## Endpoint for deleting a specific device from a user's profile page.
## Returns the updated content for the devices div in the profile page.
def delete_device(request):
    device_id = request.GET['device_id']
    device = UserDevice.objects.get(pk=device_id)
    device.delete()
    user_id = request.GET['user_id']
    devices = UserDevice.objects.filter(user_profile=user_id)
    return render(request, 'devices.html', {'devices':devices})


## Deletes a user's userdevice objects, then deletes that user's userprofile.
def delete_user(request):
    user_id = request.GET['user_id']
    userprofile=UserProfile.objects.get(pk=user_id)
    devices = UserDevice.objects.filter(user_profile=userprofile)
    for device in devices:
        device.delete()
    userprofile.delete()
    users = UserProfile.objects.all()
    return render(request, 'users.html', {'userprofiles':users})


def about(request):
    return render(request, 'about.html')
