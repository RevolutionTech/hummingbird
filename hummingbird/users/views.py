from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import Template, RequestContext
from django.template.loader import get_template
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import View

from hummingbird.settings import FEEDBACK_EMAIL as feedback_email
import config
from utils import create_kwargs
from users.admin import UserManager
from users.models import User, UserProfile
from songs.models import Song
from network.models import ActivityLog

class UserView(View):
	def __init__(self):
		self.um = UserManager()

	def init_hummingbird(self, request):
		self.um.init_hummingbird()
		return HttpResponseRedirect('/')

	def get_songs(self):
		return [{
			'id': song.id,
			'title': song.title,
			'artist': song.artist,
			'album': song.album,
			'length': config.time_default_max_song_length,
		} for song in Song.objects.all().order_by('title')]

	def login(self, request):
		def verify_user_identity(login_email, login_password):
			user_emails = User.objects.filter(email=login_email)
			for user_email in user_emails:
				try:
					username = User.objects.get(email=login_email).username
				except User.DoesNotExist:
					continue
				user = authenticate(username=username, password=login_password)
				if user:
					return user
			user_usernames = User.objects.filter(username=login_email)
			for user_username in user_usernames:
				user = authenticate(username=login_email, password=login_password)
				if user:
					return user
			return None
		
		# Check if user is already authenticated
		if request.user.is_authenticated():
			return HttpResponseRedirect('/activity')
		# Check POST data to see if login information is present
		elif 'login_email' in request.POST:
			params = [	('login_email', unicode),
						('login_password', unicode),]
			kwargs = create_kwargs(request=request, params=params)
			user = verify_user_identity(**kwargs)
			if user:
				login(request, user)
				return HttpResponseRedirect('/activity')
		# Check POST data for create account information
		elif 'create_email' in request.POST:
			params = [	('create_email', unicode, False),
						('create_mac_address', unicode, False),
						('create_first_name', unicode, False),
						('create_last_name', unicode),
						('create_username', unicode),
						('create_password', unicode),
						('create_password_confirm', unicode),
						('create_delay', int),
						('create_song_id', int),]
			kwargs = create_kwargs(request=request, params=params)
			userprofile = self.um.create_user(**kwargs)
			
			password = kwargs['create_password'] if ('create_password' in kwargs and kwargs['create_password'] != '') else kwargs['create_mac_address']
			user = authenticate(username=userprofile.user.username, password=password)
			login(request, user)
			return HttpResponseRedirect('/activity')

		# If all else fails, present the login screen
		html = get_template('login.html').render(RequestContext(request, {
			'songs': self.get_songs(),
			'delay': config.time_default_delay_to_play_song,
			'feedback_email': feedback_email,
		}))
		return HttpResponse(html)

	def logout(self, request):
		logout(request)
		return HttpResponseRedirect('/')

	def activity(self, request):
		if not request.user.is_authenticated():
			return HttpResponseRedirect('/')

		num_messages = ActivityLog.objects.all().count()
		activity_log = ActivityLog.objects.all().order_by('id')
		if num_messages > config.activity_events_per_page:
			activity_log = activity_log[num_messages-config.activity_events_per_page:]
		messages = [{
			'id': message.id,
			'date': message.date,
			'message': message.message,
		} for message in activity_log]
		
		html = get_template('activity.html').render(RequestContext(request, {
			'log_messages': messages,
			'feedback_email': feedback_email,
		}))
		return HttpResponse(html)

	def profile(self, request):
		if not request.user.is_authenticated():
			return HttpResponseRedirect('/')
		
		# Get basic data from webpage
		params = [	('first_name', unicode),
					('last_name', unicode),
					('email', unicode),
					('mac_address', unicode),
					('username', unicode),
					('password', unicode),
					('password_confirm', unicode),
					('song_id', int),
					('delay', int),]
		kwargs = create_kwargs(request=request, params=params)

		# Get song upload from webpage
		if 'song_choice' in request.POST:
			if request.POST['song_choice'] != 'select' and 'song_id' in kwargs:
				del kwargs['song_id']
			if request.POST['song_choice'] == 'upload' and 'song_upload' in request.FILES:
				kwargs['song_upload'] = request.FILES['song_upload']

		up = request.user.userprofile
		if kwargs:
			kwargs['user'] = up

			# Update data
			self.um.update_user(**kwargs)

		# Post data to webpage
		html = get_template('profile.html').render(RequestContext(request, {
			'firstName': up.user.first_name,
			'lastName': up.user.last_name,
			'email': up.user.email,
			'MAC': up.mac_address,
			'username': up.user.username,
			'songs': self.get_songs(),
			'walkin_song': up.walkin_song.song.id,
			'delay': up.delay,
			'feedback_email': feedback_email,
		}))
		return HttpResponse(html)
