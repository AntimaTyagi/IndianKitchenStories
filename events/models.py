from django.db import models
from django.utils.functional import empty
from datetime import datetime
import datetime
import os
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from payments.models import EventBuy
from django.db.models.deletion import CASCADE
from accounts.models import User

def get_file_path(instance, filename):
    now=datetime.now()
    return os.path.join("images",f"events/{instance.title}/{now.year}/{now.month}/{now.day}/",filename)

class EventModel(models.Model):
    title=models.CharField(max_length=50)
    description=models.TextField(null=True)
    image=models.ImageField(upload_to=get_file_path)
    start_date=models.DateField(null=False, blank=False)
    end_date=models.DateField(null=False,blank=False)
    price=models.IntegerField(blank=True, null=True)
    

    def __str__(self):
        return self.title+"| "+str( self.price)

    def get_display_price(self):
        return "{0:.2f}".format(self.price/100) 
    def clean_date(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        if end_date < start_date:
            raise models.ValidationError("End date should be greater than start date.")


    def save(self, *args, **kwargs):
        is_new = True if not self.id else False
        super(EventModel, self).save(*args, **kwargs)
        if is_new:
            order = EventBuy(name=self.title, price=self.price)
            order.save()


@receiver(post_delete, sender=EventModel)
def auto_delete_file_on_delete(sender, instance,**kwargs):
    if instance.file:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@receiver(pre_save, sender=EventModel)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False
    try:
        old_file= sender.objects.get(pk=instance.pk).image

    except sender.DoesNotExist:
        return False
    new_file=instance.image
    if not new_file==old_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


class FeedbackCommentModel(models.Model):
    event_id=models.ForeignKey(EventModel,on_delete=CASCADE, null=False,  verbose_name = 'eventId', related_name='eventId')
    feedback=models.CharField(max_length=275, blank=False)
    userId=models.ForeignKey(User,on_delete=CASCADE, null=False,  verbose_name = 'reviewcommenter', related_name='reviewcommenter')
    created_date=models.DateField( default=datetime.date.today)
    modified_date=models.DateField(null=False,blank=False)



