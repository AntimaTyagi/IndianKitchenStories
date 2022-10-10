from django.urls import path
from .views import DraftsListView, PostCreateView, PostUpdateView,PostListView, PostDetailView,CategoriesCreateView


app_name="blogs"
urlpatterns = [
    path('create',PostCreateView.as_view(),name='blog-create'),
    path('update/<str:slug>/', PostUpdateView.as_view(),name='blog-update'),
    path('',PostListView.as_view(),name='blog-list'),
    path('drafts/',DraftsListView.as_view(),name='drafts'),
    path('<slug:slug>',PostDetailView.as_view(),name='blog-details'),
    path('categories/',CategoriesCreateView.as_view(),name='blog-categories'),
    
]
