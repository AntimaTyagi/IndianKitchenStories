from django.urls import path
from .views import EventCreateView, EventListView,FeedbackCreateView,feedback_list_view_user

app_name="events"
urlpatterns = [
    path('create_event/',EventCreateView.as_view(), name='create_event'),
    path('',EventListView.as_view(),name='event_list'),
    path('feedback/',FeedbackCreateView.as_view(), name='create_feedback' ),
    path('feedback/<int:pk>/',feedback_list_view_user, name='view_feedback' )
    
]
