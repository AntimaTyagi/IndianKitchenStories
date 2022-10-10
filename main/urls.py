from django.urls import path
from .views import Mainview
from .import views

app_name="home"
urlpatterns = [
    path('',views.Mainview.as_view(),name="home"),
    path('about-us',views.AboutUsView.as_view(),name='about-us'),
    path('contact-us',views.ContactUsView.as_view(),name="contact-us"),

]