from django.contrib import admin
from models import UserProfile, UserDevice


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_played', 'song', 'length',)


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserDevice)
