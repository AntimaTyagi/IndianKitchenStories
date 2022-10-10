

from django.contrib import admin
from .models import Category, CommentModel, PostModel

admin.site.register(Category)
admin.site.register(PostModel)
admin.site.register(CommentModel)
