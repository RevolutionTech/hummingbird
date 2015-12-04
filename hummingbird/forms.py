from django import forms
from django.contrib.auth.models import User

from models import UserProfile, UserDevice


class UserProfileForm(forms.ModelForm):

	class Meta:
		model = UserProfile
		fields = ('name', 'song', 'length')


class UserDeviceForm(forms.ModelForm):

	class Meta:
		model = UserDevice
		fields = ('mac_id',)


class UserSongForm(forms.ModelForm):

	class Meta:
		model = UserProfile
		fields = ('song', 'length',)


class UserForm(forms.ModelForm):

	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'email', 'password',)
