from django.test import TestCase
from users.models import User
from users.views import distance_between, get_nearest_users

import json


class UserTestCase(TestCase):

    def setUp(self):
        user_id = 1
        json_data = open('users/randomLocations.json').read()
        data = json.loads(json_data)
        locations = data.get('randomLocations')
        token = input("enter your token: ")
        for i in range(len(locations)):
            location = locations[i]
            lat = location.get('lat')
            lon = location.get('lon')

            User.objects.create(user_id=i,
                                location_lon=lon,
                                location_lat=lat,
                                token=token)

    def testGetNearestUsers(self):
        print("testing function get_nearest_users for trivial data\n...")
        first_user = User.objects.first()
        nearest_users_ids = [5,1,9,2,6]
        # print("distances to user {}:".format(first_user.user_id))
        for user in User.objects.all():
            if not (user == first_user):
                distance = distance_between(first_user, user)
                # print("distance between user {} and user {} is {}m ".format(first_user.user_id, user.user_id, distance))
        response = get_nearest_users(first_user)
        response_ids = []
        for user in response:
            response_ids.append(int(user.user_id))

        self.assertEqual(nearest_users_ids, response_ids)
        print("test succesful")
