from django.db import models

class User(models.Model):
    user_id = models.CharField(max_length=200, blank=False)
    location_lon = models.FloatField(blank=False)
    location_lat = models.FloatField(blank=False)
    current_track_id = models.CharField(max_length=100, default=-1)
    nearest_users = models.ManyToManyField('self')
    token = models.CharField(max_length=200, default=-1)
    preview_url = models.URLField(default=-1)
    playlist_id = models.CharField(max_length=100,default=-1)

    def __str__(self):
        return self.user_id
