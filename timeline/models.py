from django.db import models
from django.contrib.auth.models import AbstractUser, User
from datetime import datetime

# Create your models here.
class UserFollowing(models.Model):
    user = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    following_user = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    # user_id follows following_user
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id','following_user_id'],  name="unique_followers")
        ]
        ordering = ["-created"]

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date_time = models.DateTimeField(default=datetime.now, blank=True)
    content = models.TextField(max_length=500)

class Reply(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date_time = models.DateTimeField(default=datetime.now, blank=True)
    content = models.TextField(max_length=200)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
