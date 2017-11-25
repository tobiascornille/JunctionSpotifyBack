from django.http import HttpResponse
from polls.models import User
# pip install gpxpy --user
import gpxpy.geo
import json
import spotipy
import sys
import spotipy.util as util

def get_nearest_users(current_user_id):
    current_user = User.objects.filter(user_id=current_user_id).first()
    print(current_user)
    current_user_lon = current_user.location_lon
    current_user_lat = current_user.location_lat
    users = User.objects.all()
    nearest_users = []
    for i in range(0,5):
        closest = None
        for u in users:
            if u != current_user and u not in nearest_users:
                if closest == None:
                    closest = u
                else:
                    closest = nearest_user(current_user, closest, u)
        nearest_users.append(closest)

    return nearest_users

# helper function
def nearest_user(current, u1, u2):
    u1_lon = u1.location_lon
    u1_lat = u1.location_lat

    u2_lon = u2.location_lon
    u2_lat = u2.location_lat

    c_lon = current.location_lon
    c_lat = current.location_lat

    dist_u1 = gpxpy.geo.haversine_distance(u1_lat, u1_lon, c_lat, c_lon)
    dist_u2 = gpxpy.geo.haversine_distance(u2_lat, u2_lon, c_lat, c_lon)

    if (dist_u1 < dist_u2):
        return u1
    else:
        return u2

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
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print ("Whoops, need your username!")
        print ("usage: python user_playlists.py [username]")
        sys.exit()

    token = util.prompt_for_user_token(username)
    output = ""

    if token:
        sp = spotipy.Spotify(auth=token)
        playlists = sp.user_playlists(username)
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
    return HttpResponse(output)

def POST(request):
    data = json.load(request)
    print(JsonRepsponse(data=data))
    return JsonRepsponse(data=data)

    # #PROCESS THE POST REQUEST @TOBIAS
    # @api_view(['POST'])
    # def post_location(request, format=None):
