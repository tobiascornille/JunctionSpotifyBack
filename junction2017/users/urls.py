from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^update', views.update_user),
    url(r'^callback', views.authentication_spotify),
    url(r'^([\w.@+-]+)', views.user_data, name='user_data'),
    url(r'^$', views.create_user),
    # url(r'^postrequest', views.GET),
    # url(r'^spotipy', views.get_tracks)
]
