"""recipes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('recipes/', include('recipes.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import RecipeCreateView, RecipeView, search, categoryView, recipedetail,CategoryListView



app_name='recipes'
urlpatterns = [
    path('', RecipeView.as_view(), name="recipe"),
    path('search/', search, name="search"),
    path('category/<str:cats>/', categoryView, name="category"),
    path('category',CategoryListView.as_view(),name="category-list"),
    path('recipe/<slug:slug>/', recipedetail.as_view(), name="recipe-detail"),
    path('create/',RecipeCreateView.as_view(),name='recipe-create'),
]

# urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
