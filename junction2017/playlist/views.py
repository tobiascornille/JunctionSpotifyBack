from users.models import User
import spotipy
#import rest_framework

#@api_view(['POST'])
def create_playlist(request, user_id):
    # Create a new playlist
    user = User.objects.filter(user_id=user_id).first()
    token = user.token
    if token:
        spotify = spotipy.Spotify(auth=token)
        playlist = spotify.user_playlist_create(user_id, "Cirkel")
        user.playlist_id = playlist["id"]
        user.save


#@api_view(['POST', 'DELETE'])
def modify_track(request):
    # Add or delete a track to the user's playlist
    decoded_response = request.body.decode('utf-8')
    item = json.loads(decoded_response)
    user_id = item["user_id"]
    track_id = item["track_id"]
    user = User.objects.filter(user_id=user_id).first()
    token = user.token
    playlist_id = user.playlist

    if token:
        spotify = spotipy.Spotify(auth=token)
        results="Somethings wrong :/"

        if request.method == 'POST':
            results = spotify.user_playlist_add_tracks(user_id, playlist_id, list(track_id))
        elif request.method == 'DELETE':
            results = user_playlist_remove_all_occurrences_of_tracks(user_id, playlist_id, list(track_id))
