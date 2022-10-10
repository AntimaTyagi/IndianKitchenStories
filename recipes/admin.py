from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import Post, Categories

# Register your models here.
admin.site.unregister(Group)
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Categories)
