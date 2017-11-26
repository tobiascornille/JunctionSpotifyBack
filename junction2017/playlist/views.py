from django.http import HttpResponse
from users.models import User
import spotipy
import json
# from rest_framework.decorators import api_view

#@api_view(['POST'])
def create_playlist(request):
    # Create a new playlist
    decoded_response = request.body.decode('utf-8')
    user_id = json.loads(decoded_response)["user_id"]
    user = User.objects.filter(user_id=user_id).first()
    token = user.token

    if token:
        spotify = spotipy.Spotify(auth=token)
        playlist = spotify.user_playlist_create(user_id, "Cirkel")
        user.playlist_id = playlist["id"]
        user.save()
        return HttpResponse(playlist)
    return HttpResponse("Fail")


#@api_view(['POST', 'DELETE'])
def modify_track(request):
    # Add or delete a track to the user's playlist
    decoded_response = request.body.decode('utf-8')
    item = json.loads(decoded_response)
    user_id = item["user_id"]
    track_id = item["track_id"]
    tracks = [track_id]
    user = User.objects.filter(user_id=user_id).first()
    token = user.token
    playlist_id = user.playlist_id
    results="Somethings wrong :/"

    if token:
        spotify = spotipy.Spotify(auth=token)
        if request.method == 'POST':
            results = spotify.user_playlist_add_tracks(user_id, playlist_id, tracks)
        elif request.method == 'DELETE':
            results = spotify.user_playlist_remove_all_occurrences_of_tracks(user_id, playlist_id, tracks)

    return HttpResponse(results)
