from django.db import models


class Video(models.Model):
    title = models.CharField(max_length=200)
    video_id = models.CharField(max_length=200)
    description = models.CharField(max_length=500)

