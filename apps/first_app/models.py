from __future__ import unicode_literals

from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=38)
    last_name = models.CharField(max_length=38)
    password = models.CharField(max_length=38)
    email = models.CharField(max_length=60)

class Secret(models.Model):
    message = models.TextField(max_length=1000)
    user_id = models.ForeignKey(User)
    likes = models.ManyToManyField(User, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
