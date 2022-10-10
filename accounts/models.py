from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager
import os
from datetime import datetime
from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save, pre_save

def get_file_path(instance, filename):
    now=datetime.now()
    return os.path.join("images",f"{instance.email}/",filename)

class User(AbstractUser):
    ADMIN = 'ADMIN'
    SUBSCRIBER = 'SUBSCRIBER'
    FOLLOWER='FOLLOWER'

    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (SUBSCRIBER, 'Subscriber'),
        (FOLLOWER,'follower'),
    )

    username = None
    email = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    profile_photo = models.ImageField(upload_to=get_file_path, blank=True, default="profile_default.png")
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    first_name = models.CharField(max_length=100,default="")
    last_name = models.CharField(max_length=100,default="")
    phone_no= models.CharField(max_length=100,default="")
    is_email_verified = models.BooleanField(default=False)
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email


@receiver(post_delete, sender=User)
def auto_delete_file_on_delete(sender, instance,**kwargs):
    if instance.profile_photo:
        if os.path.isfile(instance.profile_photo.path):
            os.remove(instance.profile_photo.path)


@receiver(pre_save, sender=User)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False
    try:
        old_file= sender.objects.get(pk=instance.pk).profile_photo
        # print("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")

    except sender.DoesNotExist:
        return False
    new_file=instance.profile_photo
    if not new_file==old_file or old_file is None:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


