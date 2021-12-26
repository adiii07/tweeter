from django.contrib import admin
from django.contrib.auth.models import User
from timeline.models import Post, Reply, UserFollowing

# Register your models here.
admin.site.register(Post)
admin.site.register(Reply)
admin.site.register(UserFollowing)
