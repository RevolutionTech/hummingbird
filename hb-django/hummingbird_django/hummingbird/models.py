from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class UserProfile(models.Model):
	name = models.CharField(max_length=40, null=True)
	last_played = models.DateTimeField(null=True, blank=True)
	song = models.FileField(upload_to='media/songs', null=True, blank=True)
	length = models.IntegerField(default=10,
				validators=[
				MaxValueValidator(120),
				MinValueValidator(1)
				]
			)

	def __unicode__(self):
		return str(self.name) + " - " + str(self.song)


class UserDevice(models.Model):
	user_profile = models.ForeignKey(UserProfile, null=True)
	mac_id = models.CharField(max_length=20, unique=True)

	def __unicode__(self):
		return self.mac_id