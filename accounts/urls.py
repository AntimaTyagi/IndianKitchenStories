from os import name
from django.contrib.auth import views as auth_views
from django.urls.base import reverse_lazy

from .views import LoginPageView, signup_page
from django.contrib.auth.views import  LogoutView
from django.urls import path 
from .import  views
from .views import SubscribingView
app_name='accounts'
urlpatterns = [
    path("login/",LoginPageView.as_view(template_name='accounts/login.html'),name="login"),
    path("logout/",LogoutView.as_view(),name="logout"),
    path('signup/',views.signup_page ,name='signup'),
    path('activate-user/<uidb64>/<token>',
         views.activate_user, name='activate'),
    path('<pk>/subscribing',SubscribingView.as_view(),name="subcreate"),
]
