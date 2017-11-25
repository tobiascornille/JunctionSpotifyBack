from django.http import HttpResponse
from users.models import User
# pip install gpxpy --user
import gpxpy.geo
import json
import spotipy
import sys
import spotipy.util as util
import math
import colorsys
import requests


def user_data(request, user_id, location_lat, location_lon):
    # get current_user
    current_user = User.objects.all().filter(user_id=user_id).first()
    # update location
    current_user.location_lat = location_lat
    current_user.location_lon = location_lon
    # API call for current_track_id
    current_track_id = get_current_track()
    # define 5 nearest_users
    nearest_users = get_nearest_users(current_user.user_id)
    #update nearest users
    current_user.nearest_users = nearest_users
    # save changes to current user in database
    current_user.save()
    # return those 5
    return HttpResponse(to_json(current_user, nearest_users))

def get_nearest_users(current_user_id):
    current_user = User.objects.filter(user_id=current_user_id).first()
    current_user_lon = current_user.location_lon
    current_user_lat = current_user.location_lat
    users = User.objects.all()
    nearest_users = []
    if len(users) < 6:
        limit_users = len(users) - 1
    else:
        limit_users = 5
    for i in range(0, limit_users):
        min_distance = math.inf
        closest_user = None
        for user in users:
            if user != current_user and user not in nearest_users:
                distance = distance_between(current_user, user)
                if distance < min_distance:
                    min_distance = distance
                    closest_user = user
        nearest_users.append(closest_user)

    return nearest_users

# helper function
def distance_between(u1, u2):
    u1_lon = u1.location_lon
    u1_lat = u1.location_lat

    u2_lon = u2.location_lon
    u2_lat = u2.location_lat

    return gpxpy.geo.haversine_distance(u1_lat, u1_lon, u2_lat, u2_lon)

def return_json(request):
    response_data = {}
    response_data['name'] = ('name')
    for i in range(0,5):
        response_data['track' + i] = ('track id')

    return JsonRepsponse({'foo':'bar'})

def get_colour(track_id):
    spotify = spotipy.Spotify()
    track = spotify.track(track_id)
    trackFeatures = spotify.audio_features(trackId)

    trackEnergy = trackFeatures[0]['energy']
    trackTempo = trackFeatures[0]['tempo']
    trackValence = trackFeatures[0]['valence']

    hue = energy * 360;
    saturation = convert_tempo(tempo);
    value = valence;
    colour = tuple(int(i * 255) for i in colorsys.hsv_to_rgb(hue, saturation, value))
    return colour

def convert_tempo(tempo):
    tempovalue = 0
    if tempo <= 40:
        tempovalue = 40
    elif tempo >= 170:
        tempovalue = 170
    else:
        tempovalue = tempo

    tempovalue -= 40

    tempovalue = tempovalue / 130

    return tempovalue


def get_current_track():
    scope = "user-library-read user-read-private user-read-email user-read-birthdate"
    # c_id =  '7f6e830e710d4157b2b47a6a76fb7cf5'
    # c_secret = '65ab11b0ad8c43feb801be2675dc175c'
    c_id = 'a42f6a4a96e749ddb4b2cc5ee306ee8e'
    c_secret = '241d01abfd024f749977e2c58fd1e299'
    uri = 'https://localhost:8888/callback'
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print ("Whoops, need your username!")
        print ("usage: python user_playlists.py [username]")
        sys.exit()

    token = util.prompt_for_user_token(username, scope, client_id=c_id, client_secret=c_secret,redirect_uri=uri)
    output = ""
    if token:
        sp = spotipy.Spotify(auth=token)
        current_song = sp.current_user_playing_track()
        current_song_id = current_song['item']['id']
        return current_song_id

    print("something went wrong")
    return None

def get_current_track_name(user_id):
    user = User.objects.filter(user_id=user_id).first()
    track_id = user.current_track_id
    token  = user.token
    output = ""
    if token:
        spotify = spotipy.Spotify(auth=token)
        track = spotify.track(track_id)
        track_name = track['name']
        return track_name

    print("something went wrong")
    return None


#helper

def to_json(current_user, nearest_users):
    json_output = {}
    json_output['nearest_users'] = []
    for user in nearest_users:
        user_data = {}
        user_data['track_id'] = user.current_track_id
        user_data['track_name'] = get_current_track_name(user.user_id)
        user_data['track_color'] = get_colour(user.current_track_id)
        json_output['nearest_users'].append(user_data)
    json_output['current_track_id'] = current_user.current_track_id
    json_output['current_track_name'] = get_current_track_name(user.user_id)
    json_output['current_track_color'] = get_colour(current_user.current_track_id)
    return json_output

def create_user(request, ):
    item = json.loads(decoded_response)
    user_id = item.get("user_id")
    location_lon = item.get("location_lat")
    location_lat = item.get("location_lat")

    new_user = User(user_id=user_id, location_lon=location_lon, location_lat=location_lat, token=token, track_color=track_color, current_track_id=current_track_id,nearest_users=nearest_users, preview_url=preview_url)

    return True
