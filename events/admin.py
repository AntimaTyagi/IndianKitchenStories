from django.contrib import admin
from .models import EventModel,FeedbackCommentModel

admin.site.register(EventModel)
admin.site.register(FeedbackCommentModel)