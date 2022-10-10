from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date
#from ckeditor.fields import RichTextField
from django.db.models.base import Model
from django.db.models.signals import pre_save
from recipes.utils import unique_slug_generator
from django.conf import settings
import os
from taggit.managers import TaggableManager

def get_file_path(instance, filename):
    now=datetime.now()
    return os.path.join("images",f"recipes/categorie/{instance.categoryname}/",filename)
def get_recipe_path(instance, filename):
    now=datetime.now()
    return os.path.join("images",f"recipes/{instance.title}/",filename)

class Categories(models.Model):
    categoryname = models.CharField(max_length=70)
    description=models.CharField(max_length=150, null=True,blank=True)
    icon=models.ImageField(blank=True,null=True, upload_to=get_file_path)
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.categoryname

class Post(models.Model):
    title = models.CharField(max_length=255)
    title_tag = models.CharField(max_length=255, default='Recipe Post')
    slug = models.SlugField(max_length=255, null=True, blank=True)
    #author = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    img = models.ImageField(upload_to=get_recipe_path, null=True)
    body = models.TextField(blank= True, null= True)
    ingredients = TaggableManager()
    post_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Categories, null=True, on_delete=models.PROTECT, related_name='category_set')

    def __str__(self):
        return self.title + ' | ' + str(self.author)

def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(slug_generator, sender=Post)