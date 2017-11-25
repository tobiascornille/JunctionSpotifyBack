from django.http import HttpResponse
from users.models import User
# pip install gpxpy --user
import gpxpy.geo
import json
import math

import sys
import spotipy
import spotipy.util as util

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

def get_tracks(request):
    scope = 'user-library-read'
    output=""

    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        output += "<h1>Usage:" + str(sys.argv([0])) + "username</h1><br>"
        sys.exit()

    token = util.prompt_for_user_token(username, scope, client_id='7f6e830e710d4157b2b47a6a76fb7cf5',client_secret='65ab11b0ad8c43feb801be2675dc175c',redirect_uri='http://localhost:8000/users/spotipy')

    if(token):
        sp = spotipy.Spotify(auth=token)
        results = sp.current_user_saved_tracks()
        for item in results['items']:
            track = item['track']
            output += "<h2>" + str(track['name']) + ' - ' + str(track['artists'][0]['name']) + "</h2><br>"
    else:
        output += "<h2>Can't get token for " + str(username) + "</h2<br>"
    return HttpResponse(output)

def GET(request):
    data = json.load(request)
    print(JsonRepsponse(data=data))
    return JsonRepsponse(data=data)

    # #PROCESS THE POST REQUEST @TOBIAS
    # @api_view(['POST'])
    # def post_location(request, format=None):
