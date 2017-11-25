from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^postrequest', views.GET),
    url(r'^spotipy', views.get_tracks)
]
