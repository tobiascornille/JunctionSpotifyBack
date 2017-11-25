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

def index(request):
    output = ""
    current_user = User.objects.first()
    if current_user == None:
        return HttpResponse("no users")
    data = get_nearest_users(current_user.user_id)
    for i in data:
        output += "<h1>"+str(i.user_id)+"</h1><br>"
    return HttpResponse(output)

def show_tracks(request):
    output = ""
    for i, item in enumerate(tracks['items']):
        track = item['track']
        output += "<h1>" + str(track['artists'][0]['name']) + '</h1><br>' + '<h1>' + str(track['name']) + '</h1><br>'
    return output

def get_tracks(request):
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
        playlists = sp.user_playlists(username)
        output += '<h1>' + str(sp.me()['display_name']) + '</h1><br>'
        for playlist in playlists['items']:
            if playlist['owner']['id'] == username:
                results = sp.user_playlist(username, playlist['id'],
                    fields="tracks,next")
                tracks = results['tracks']
                output += show_tracks(tracks)
                while tracks['next']:
                    tracks = sp.next(tracks)
                    output += show_tracks(tracks)
    else:
        output = "something went wrong"

    get_trackFeatures(sp)
    return HttpResponse(output)

def POST(request):
    data = json.load(request)
    print(JsonRepsponse(data=data))
    return JsonRepsponse(data=data)

def return_json(request):
    response_data = {}
    response_data['name'] = ('name')
    for i in range(0,5):
        response_data['track' + i] = ('track id')

    return JsonRepsponse({'foo':'bar'})

def get_trackFeatures(sp):
    trackId = sp.current_user_playing_track()['item']['id']
    trackFeatures = sp.audio_features(trackId)
    print(trackFeatures)
    trackEnergy = trackFeatures[0]['energy']
    trackTempo = trackFeatures[0]['tempo']
    trackValence = trackFeatures[0]['valence']

    print(trackEnergy)
    print(trackTempo)
    print(trackValence)



def get_colour(energy, tempo, valence):
    hue = energy * 360;
    saturation = convert_tempo(tempo);
    value = valence;

    colour = hsv_to_rgb(hue, saturation, value)

    return colour

def convert_tempo(tempo):
    tempovalue = 0
        if tempo <= 40
            tempovalue = 40
        else if tempo >= 170
            tempovalue = 170
        else
            tempovalue = tempo

    tempovalue -= 40

    tempovalue = tempovalue / 130

    return tempovalue

    # #PROCESS THE POST REQUEST @TOBIAS
    # @api_view(['POST'])
    # def post_location(request, format=None):
