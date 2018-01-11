import django
from users.models import User
from random import randrange

if __name__ == "__main__":
    django.setup()

def fill_db():
    User.objects.all().delete()

    for i in range(0,50):
        rand_lon = randrange(360)
        rand_lat = randrange(180)
        track_id = '11dFghVXANMlKmJXsNCbNl'
        new_user = User(user_id=i, location_lon=rand_lon, location_lat=rand_lat, current_track_id=track_id)
        new_user.save()
