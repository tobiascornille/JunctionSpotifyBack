from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^$', views.create_playlist, name='playlist'),
        url(r'^track$', views.modify_track, name='playlist-track'),
]
