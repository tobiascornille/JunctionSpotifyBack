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

def index(request):
    request_body = json.loads(request.body)
    current_user = User(
        user_id=request_body["user_id"],
        location_lon=request_body["location_lon"],
        location_lat=request_body["location_lat"],
    )
    output = ""
    data = get_nearest_users(current_user.user_id)
    for i in data:
        output += "<h1>"+str(i.user_id)+"</h1><br>"
    return HttpResponse(output)

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

# def get_trackFeatures(sp):
#     track = sp.current_user_playing_track()
#     trackId = track['item']['id']
#     trackFeatures = sp.audio_features(trackId)
#     print(trackFeatures)
#     trackEnergy = trackFeatures[0]['energy']
#     trackTempo = trackFeatures[0]['tempo']
#     trackValence = trackFeatures[0]['valence']
#
#     print(trackEnergy)
#     print(trackTempo)
#     print(trackValence)
#     print("colour")
#     print(get_colour(trackEnergy, trackTempo, trackValence))

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

#test function
# def get_tracks(request):
#     scope = "user-library-read user-read-private user-read-email user-read-birthdate"
#     # c_id =  '7f6e830e710d4157b2b47a6a76fb7cf5'
#     # c_secret = '65ab11b0ad8c43feb801be2675dc175c'
#     c_id = 'a42f6a4a96e749ddb4b2cc5ee306ee8e'
#     c_secret = '241d01abfd024f749977e2c58fd1e299'
#     uri = 'https://localhost:8888/callback'
#     if len(sys.argv) > 1:
#         username = sys.argv[1]
#     else:
#         print ("Whoops, need your username!")
#         print ("usage: python user_playlists.py [username]")
#         sys.exit()
#
#     token = util.prompt_for_user_token(username, scope, client_id=c_id, client_secret=c_secret,redirect_uri=uri)
#     output = ""
#     if token:
#         sp = spotipy.Spotify(auth=token)
#         playlists = sp.user_playlists(username)
#         output += '<h1>' + str(sp.me()['display_name']) + '</h1><br>'
#         for playlist in playlists['items']:
#             if playlist['owner']['id'] == username:
#                 results = sp.user_playlist(username, playlist['id'],
#                     fields="tracks,next")
#                 tracks = results['tracks']
#                 output += show_tracks(tracks)
#                 while tracks['next']:
#                     tracks = sp.next(tracks)
#                     output += show_tracks(tracks)
#     else:
#         output = "something went wrong"
#
#     get_trackFeatures(sp)
#     return HttpResponse(output)

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

def get_current_track_name():
    spotify = spotipy.Spotify()
    track = spotify.track(get_current_track())
    track_name = track['name']

# def show_tracks(request):
#     output = ""
#     for i, item in enumerate(tracks['items']):
#         track = item['track']
#         output += "<h1>" + str(track['artists'][0]['name']) + '</h1><br>' + '<h1>' + str(track['name']) + '</h1><br>'
#     return output

def GET(request):
    # retrieve id and location
    data = json.load(request.body)

    user_id = data['user_id']
    location_lat = data['location_lat']
    location_lon = data['location_lon']
    # get current_user
    current_user = User.objcets.all().filter(user_id=user_id)
    # update location
    current_user.location_lat = location_lat
    current_user.location_lon = location_lon
    # API call for current_track_id
    current_track_id = get_current_track()
    # define 5 nearest_users
    nearest_users = get_nearest_users(currrent_user.user_id)
    #update nearest users
    current_user.nearest_users = nearest_users
    # save changes to current user in database
    current_user.save()
    # return those 5
    return to_json(current_user, nearest_users)

#helper

def to_json(current_user, nearest_users):
    json_output = {}
    json_output['nearest_users'] = []
    for user in nearest_users:
        user_data = {}
        user_data['track_id'] = user.user_id
        #TODO
        user_data['track_name'] =
        user_data['track_color'] = get_colour(user.user_id)
        json_output['nearest_users'].append(user_data)
    json_output['current_track_id'] = current_user.user_id
    #TODO
    json_output['current_track_name']
    json_output['current_track_color'] = get_colour(current_user.user_id)
    return json_output

#unused
# def POST(request):
#     data = json.load(request)
#     print(JsonRepsponse(data=data))
#     return JsonRepsponse(data=data)
