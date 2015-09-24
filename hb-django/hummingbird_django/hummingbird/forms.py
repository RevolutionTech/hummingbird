from django import forms
from models import UserProfile, UserDevice
from django.contrib.auth.models import User

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('name','song','length')

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username','email','password')