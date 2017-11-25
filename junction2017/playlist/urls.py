from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^playlist/$', views.create_playlist, name='playlist'),
        url(r'^playlist/\S+', views.modify_track, name='playlist-track'),
]
