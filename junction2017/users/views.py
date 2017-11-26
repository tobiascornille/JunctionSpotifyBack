from django.http import HttpResponse
from users.models import User
import gpxpy.geo
import json
import spotipy
import math
import colorsys
import requests
from django.shortcuts import redirect


def authentication_spotify(request):
    code = request.GET.get('code',None)
    print("code")
    print(code)
    print()

    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://95.85.31.26/users/callback",
        "client_id": "e66d17b67e584655926e41426c2a5d15",
        "client_secret": "fd192986fc93475983541c7ff4634b18",
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    r = requests.post("https://accounts.spotify.com/api/token", data=payload, headers=headers)

    token = r.json()["access_token"]
    print("token")
    print(token)
    print()

    spotify = spotipy.Spotify(auth=token)

    user_id = spotify.current_user()["id"]


    new_user = User(user_id=user_id, token=token)

    new_user.save()

    current_track_id = get_current_track(user_id)
    new_user.current_track_id = current_track_id

    if current_track_id != None:
        track = spotify.track(current_track_id)
        new_user.preview_url = track['preview_url']

    new_user.save()

    return redirect('https://sebastianjvf.github.io/junction-spotify-front/', {'user_id':user_id})


# GET request endpoint: users/ID&lat&lon
def user_data(request, user_id):
    current_user = User.objects.all().filter(user_id=user_id).first()
    nearest_users = current_user.nearest_users
    json_output = {}
    json_output['nearest_users'] = []
    for user in nearest_users.all():
        user_data = {}
        user_data['track_id'] = user.current_track_id
        user_data['track_name'] = get_current_track_name(user.user_id)
        user_data['track_color'] = get_colour(user.user_id, user.current_track_id)
        user_data['url_preview'] = user.preview_url
        json_output['nearest_users'].append(user_data)
    json_output['current_track_id'] = current_user.current_track_id
    json_output['current_track_name'] = get_current_track_name(current_user.user_id)
    json_output['current_track_color'] = get_colour(current_user.user_id, current_user.current_track_id)
    json_output['url_preview'] = current_user.preview_url
    return HttpResponse(json.dumps(json_output))

# POST request endpoint: users/
def create_user(request):
    print("hey")
    payload = {
        'client_id': 'e66d17b67e584655926e41426c2a5d15',
        'client_secret': 'fd192986fc93475983541c7ff4634b18',
        'response_type': 'code',
        'redirect_uri': 'http://95.85.31.26/users/callback',
        # 'redirect_uri': 'cirkelapp.com/users/callback',
        # 'redirect_uri': 'http://95.85.31.26/users/callback',
        'scope': 'user-library-read user-read-private user-read-currently-playing user-read-recently-played playlist-modify-public playlist-modify-private',
        'show_dialog': 'true'
    }
    r = requests.get('https://accounts.spotify.com/authorize', params=payload)
    print("redirect to")
    print(r.url)
    return(redirect(r.url))

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
    current_track_id = get_current_track(user_id)
    user.current_track_id = current_track_id
    # nearest users
    user.nearest_users = get_nearest_users(user_id)
    # preview url
    if token:
        sp = spotipy.Spotify(auth=token)
        user.preview_url = sp.track(current_track_id)['preview_url']
    else:
        user.preview_url = None

    user.save()

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
            if user.user_id != current_user.user_id and user not in nearest_users:
                print("ik ben hier")
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

def get_colour(user_id, track_id):
    user = User.objects.filter(user_id=user_id).first()
    token = user.token
    if token:
        spotify = spotipy.Spotify(auth=token)
        track = spotify.track(track_id)
        trackFeatures = spotify.audio_features(track_id)

        track_energy = trackFeatures[0]['energy']
        track_tempo = trackFeatures[0]['tempo']
        track_valence = trackFeatures[0]['valence']

        hue = track_energy * 360;
        saturation = convert_tempo(track_tempo);
        value = track_valence;
        colour = tuple(int(i * 255) for i in colorsys.hsv_to_rgb(hue, saturation, value))
        return colour
    return None

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
    output = ""

    if token:
        sp = spotipy.Spotify(auth=token)
        #current_song = sp.current_user_playing_track()

        #if current_song:
        #    current_song_id = current_song['item']['id']
        #    return current_song_id

        current_song = sp.current_user_recently_played(limit=1)

        if current_song:
            current_song_id = current_song['items'][0]['track']['id']
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
