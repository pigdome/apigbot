from django.db import models
from django.utils import timezone


class ClosetPost(models.Model):
    code = models.CharField(max_length=20, null=False, unique=True)
    description = models.TextField()
    date = models.DateTimeField()
    date_frame = models.CharField(max_length=10)

    def __str__(self):
        return self.code


class ClosetImages(models.Model):
    code = models.CharField(max_length=20, null=False)
    name = models.CharField(max_length=30, null=False)
    src = models.TextField()
    thumnail = models.BooleanField(default=False)

    def __str__(self):
        return self.src
