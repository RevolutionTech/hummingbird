from django.contrib import admin
from hummingbird.models import UserProfile, UserDevice

class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('user_id','last_played','song','length',)

admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(UserDevice)
# Register your models here.
