from django.db import models

class User(models.Model):
    user_id = models.CharField(max_length=200, unique=True, blank=False)
    location_lon = models.FloatField(blank=False)
    location_lat = models.FloatField(blank=False)
    current_track_id = models.CharField(max_length=100, blank=False, default=-1)
    nearest_users = models.ManyToManyField('self')
