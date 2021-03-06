from django.conf.urls import patterns, url
import views


urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^profile/(?P<user_id>[\w\-]+)/$', views.profile, name='profile'),
        url(r'^about', views.about, name='about'),
        url(r'^get_user_from_device', views.get_user_from_device, name='get_user_from_device'),
        url(r'^build_user_from_device', views.build_user_from_device, name='build_user_from_device'),
        url(r'^update_last_played', views.update_last_played, name='update_last_played'),
        url(r'^add_user/', views.add_user, name='add_user'),
        url(r'^delete_device/', views.delete_device, name='delete_device'),
        url(r'^delete_user/', views.delete_user, name='delete_user'),
)
