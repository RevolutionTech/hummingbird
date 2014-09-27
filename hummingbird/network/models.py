from django.db import models

class ActivityLog(models.Model):
	date = models.DateTimeField(auto_now_add=True, blank=True)
	message = models.TextField()

	def __unicode__(self):
		return "{date}: {message}".format(date=self.date, message=self.message)
