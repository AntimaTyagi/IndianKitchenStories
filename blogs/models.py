import datetime
from datetime import datetime
from django.db import models
import os

from django.db.models.deletion import CASCADE
from accounts.models import User

def title_with_no_spacing(title):
    text=""
    for x in title:
        if x==' ':
            x="-"
        if ascii(x)!=32:
            text+=x
    return text

def get_file_path(instance, filename):
    now=datetime.now()
    return os.path.join("images",f"posts/{instance.author}/{instance.title}/{now.year}/{now.month}/{now.day}/",filename)


class Category(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class PostModel(models.Model):
    title=models.CharField(max_length=50)
    description=models.TextField()
    slug=models.SlugField(blank=True, unique=True, null=False)
    image=models.ImageField(upload_to=get_file_path)
    author=models.ForeignKey(User,on_delete=CASCADE, null=False,  verbose_name = 'Author', related_name='Author')
    is_published=models.BooleanField(default=False)
    published_on=models.DateField(null=True, blank=True)
    categories =models.ForeignKey(Category,blank=True, null=True,on_delete=CASCADE)
    featured = models.BooleanField(blank=True, null=True)
    comment_count = models.IntegerField(default = 0)
 
    def save(self, *args, **kwargs):
        if self.is_published is 'on':
            self.is_published is True
        else:
            self.is_published is False
        text=""
        for x in self.title:
            if x==' ':
                x="-"
            if ascii(x)!=32:
                text+=x
        self.slug=text
        now=datetime.now()
        print(f"{now.year}-{now.month}-{now.day}")
        self.published_on=f"{now.year}-{now.month}-{now.day}"        #YYYY-MM-DD
        super(PostModel, self).save(*args, **kwargs)
    def __str__(self):
        return self.title



class CommentModel(models.Model):
    comment=models.CharField(max_length=150, blank=False)
    commenter=models.ForeignKey(User,on_delete=CASCADE, null=False,  verbose_name = 'commenter', related_name='commenter')
    post=models.ForeignKey(PostModel,on_delete=CASCADE, null=False,  verbose_name = 'post', related_name='post')
    created_date=models.DateField(null=True, blank=True)
