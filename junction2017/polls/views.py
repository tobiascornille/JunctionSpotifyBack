from django.http import HttpResponse
from polls.models import User
# pip install gpxpy --user
import gpxpy.geo

def get_nearest_users(current_user_id):
    current_user = User.objects.filter(current_user_id=user_id).first()
    current_user_lon = current_user.location_lon
    current_user_lat = current_user.location_lon
    users = User.objects.all()
    nearest_users = list()
    output = ""
    for u in users:
        if len(nearest_users) <= 5:
            nearest_users.append(u)
        else:
            u_lon = u.location_lon
            u_lan = u.location_lat
            nearest_users.sort(key=lambda x: gpxpi.geo.haversine_distance(u_lat, u_lon, , current_user_lat))

    return nearest_users



    # #PROCESS THE POST REQUEST @TOBIAS
    # @api_view(['POST'])
    # def post_location(request, format=None):
