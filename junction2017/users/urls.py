from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^([\w.@+-]+)&([\w.@+-]+)&([\w.@+-]+)', views.user_data, name='user_data'),
    url(r'^$', views.create_user),
    # url(r'^postrequest', views.GET),
    # url(r'^spotipy', views.get_tracks)
]
