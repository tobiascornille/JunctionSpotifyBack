from django.http import HttpResponse
from users.models import User
# pip install gpxpy --user
import gpxpy.geo
import json
import spotipy
import sys
import spotipy.util_custom as util
import math
import colorsys
import requests
from django.shortcuts import redirect


def authentication_spotify(request):
    print("hey")
    return redirect('https://sebastianjvf.github.io/junction-spotify-front/')


# GET request endpoint: users/ID&lat&lon
def user_data(request, user_id, location_lat, location_lon):
    # get current_user
    current_user = User.objects.all().filter(user_id=user_id).first()
    # update location
    current_user.location_lat = location_lat
    current_user.location_lon = location_lon
    # API call for current_track_id
    current_track_id = get_current_track(user_id)
    # define 5 nearest_users
    nearest_users = get_nearest_users(current_user.user_id)
    #update nearest users
    current_user.nearest_users = nearest_users
    # save changes to current user in database
    current_user.save()
    # return those 5
    return HttpResponse(to_json(current_user, nearest_users))

# POST request endpoint: users/
def create_user(request):

    payload = {
        'client_id': 'e66d17b67e584655926e41426c2a5d15',
        'client_secret': 'fd192986fc93475983541c7ff4634b18',
        'response_type': 'code',
        'redirect_uri': 'http://localhost:8000/users/callback',
        # 'redirect_uri': 'cirkelapp.com/users/callback',
        # 'redirect_uri': 'http://95.85.31.26/users/callback',
        'scope': 'user-library-read user-read-private user-read-email user-read-birthdate',
        'show_dialog': 'true'
    }
    r = requests.get('https://accounts.spotify.com/authorize', params=payload)
    print("redirect to")
    print(r.url)
    return(redirect(r.url))
    # if len(sys.argv) > 1:
    #     username = sys.argv[1]
    # else:
    #     print ("Whoops, need your username!")
    #     print ("usage: python user_playlists.py [username]")
    #     sys.exit()
    #
    # token = util.prompt_for_user_token(username, scope, client_id=c_id, client_secret=c_secret,redirect_uri=uri)
    # spotify = spotipy.Spotify(auth=token)
    # print("token")
    # print(token)
    # print()
    # user_id = spotify.current_user()["id"]
    # location_lon = item["location"]["location_lon"]
    # location_lat = item["location"]["location_lat"]
    #
    #
    # new_user = User(user_id=user_id, location_lon=location_lon, location_lat=location_lat, token=token)
    #
    # new_user.save()
    #
    # new_user.nearest_users = get_nearest_users(user_id)
    # new_user.current_track_id = get_current_track(user_id)
    # if current_track_id != None:
    #     track = spotify.track(current_track_id)
    #     new_user.preview_url = track['preview_url']
    #
    # new_user.save()
    #
    # json_output = {}
    # json_output['user_id'] = user_id
    #
    # return HttpResponse(json_output)

def create_user(request):
    decoded_response = request.body.decode('utf-8')
    item = json.loads(decoded_response)
    scope = "user-library-read user-read-private user-read-email user-read-birthdate"
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
    spotify = spotipy.Spotify(auth=token)

    user_id = spotify.current_user()["id"]
    location_lon = item["location"]["location_lon"]
    location_lat = item["location"]["location_lat"]


    new_user = User(user_id=user_id, location_lon=location_lon, location_lat=location_lat, token=token)

    new_user.save()

    new_user.nearest_users = get_nearest_users(user_id)
    new_user.current_track_id = get_current_track(user_id)
    if current_track_id != None:
        track = spotify.track(current_track_id)
        new_user.preview_url = track['preview_url']

    new_user.save()

    json_output = {}
    json_output['user_id'] = user_id

    return HttpResponse(json_output)

# PUT request endpoint: users/update
def update_user(request):
    decoded_response = request.body.decode('utf-8')
    item = json.loads(decoded_response)

    user_id = item["user_id"]
    user = User.objects.filter(user_id=user_id).first()

    token = user.token
    # location
    user.location_lon = item["location"]["location_lon"]
    user.location_lat = item["location"]["location_lat"]
    user.save()
    # track
    user.current_track_id = get_current_track(user_id)
    # nearest users
    user.nearest_users = get_nearest_users(current_user.user_id)
    # preview url
    user.preview_url = item["preview_url"]

    return HttpResponse("200 Success")

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


def get_current_track(user_id):
    user = User.objects.filter(user_id=user_id).first()
    token = user.token
    # scope = "user-library-read user-read-private user-read-email user-read-birthdate"
    # # c_id =  '7f6e830e710d4157b2b47a6a76fb7cf5'
    # # c_secret = '65ab11b0ad8c43feb801be2675dc175c'
    # c_id = 'a42f6a4a96e749ddb4b2cc5ee306ee8e'
    # c_secret = '241d01abfd024f749977e2c58fd1e299'
    # uri = 'https://localhost:8888/callback'
    # if len(sys.argv) > 1:
    #     username = sys.argv[1]
    # else:
    #     print ("Whoops, need your username!")
    #     print ("usage: python user_playlists.py [username]").0
    #     sys.exit()
    #
    # token = util.prompt_for_user_token(username, scope, client_id=c_id, client_secret=c_secret,redirect_uri=uri)
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
    if token and track_id:
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

def create_user(request):
    decoded_response = request.body.decode('utf-8')
    item = json.loads(decoded_response)
    scope = "user-library-read user-read-private user-read-email user-read-birthdate"
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
    spotify = spotipy.Spotify(auth=token)

    user_id = spotify.current_user()["id"]
    location_lon = item["location"]["location_lon"]
    location_lat = item["location"]["location_lat"]


    new_user = User(user_id=user_id, location_lon=location_lon, location_lat=location_lat, token=token)

    new_user.save()

    new_user.nearest_users = get_nearest_users(user_id)
    new_user.current_track_id = get_current_track(user_id)
    if current_track_id != None:
        track = spotify.track(current_track_id)
        new_user.preview_url = track['preview_url']

    new_user.save()

    json_output = {}
    json_output['user_id'] = user_id

    return HttpResponse(json_output)

def to_json_test():
    json_output = {}
    json_output['nearest_users'] = []
    for i in range(0,5):
        user_data = {}
        user_data['track_id'] = 987645321
        user_data['track_name'] = ("Cool Song")
        user_data['track_color'] = tuple(int(i * 255) for i in colorsys.hsv_to_rgb(152, 0.5, 0.5))
        json_output['nearest_users'].append(user_data)
    json_output['current_track_id'] = 123456789
    json_output['current_track_name'] = ("Mah sang")
    json_output['current_track_color'] =  tuple(int(i * 255) for i in colorsys.hsv_to_rgb(52, 0.5, 0.5))
    return json_output
