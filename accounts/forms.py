from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm ,UserChangeForm
from django.db.models import fields
from django.forms.models import ModelForm
from .models import User


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email',"password1", "password2")


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email',)

class LoginForm(forms.Form):
    email=forms.EmailField()
    password=forms.CharField(max_length=63,widget=forms.PasswordInput)



class SubscriberForm(ModelForm):
    class Meta:
        model = User
        exclude=('password1','password2')
        fields=("first_name","last_name","phone_no", "profile_photo")
    # def save(self):
    #     data = self.cleaned_data
    #     # user = User( first_name=data['first_name'],
    #     #     last_name=data['last_name'],profile_photo=data['profile_photo'],
    #     #     phone_no=data['phone_no'])
    #     user=User.objects.get(email=self.instance.email)
    #     user.first_name=data['first_name']
    #     user.last_name=data['last_name']
    #     user.profile_photo=data['profile_photo']
    #     user.phone_no=data['phone_no']
    #     print(self.instance.email)
    #     print("______________________________________________")
    #     if user.get_role_display() is  "follower":
    #         user.get_role_display() is  "Subscriber"
    #     print(user)
    #     return user
        
