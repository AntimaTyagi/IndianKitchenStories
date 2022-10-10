from django.db import models
from django.conf import settings
import random
from accounts.models import User

from django.db.models.deletion import CASCADE


def create_new_ref_number():
        not_unique = True
        while not_unique:
            unique_ref = random.randint(1000000000, 9999999999)
            if not UserRole.objects.filter(referrence_number=unique_ref):
                not_unique = False
        return str(unique_ref)
class EventBuy(models.Model):
    name=models.CharField(max_length=100)
    price=models.IntegerField(default=0 )

    def __str__(self) -> str:
        return self.name

    def get_display_price(self):
        return "{0:.2f}".format(self.price/100)


class UserRole(models.Model):
    """Model representing a User's Role"""# ManyToManyField used because one user can have multiple roles and one role can have multiple users
    event = models.ForeignKey(EventBuy,on_delete=CASCADE, null=False,  verbose_name = 'Role', related_name='role')
    user = models.ForeignKey(User,on_delete=CASCADE, null=False,  verbose_name = 'User', related_name='user_role')
    referrence_number = models.CharField(
        max_length = 10,
        blank=True,
        editable=False,
        unique=True,
        null=True,
        default=create_new_ref_number
    )
    def __str__(self):
        return self.referrence_number
    



    # other fields goes here if needed