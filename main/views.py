from django.db import connection

from django.shortcuts import render
from django.views.generic.base import TemplateView
from blogs.models import CommentModel, PostModel
from payments.models import EventBuy
from events.models import EventModel
from recipes.models import Categories, Post
# Create your views here.
class Mainview(TemplateView):
    template_name="main/home.html"
    def get_context_data(self, **kwargs):
        context = super(Mainview, self).get_context_data(**kwargs)
        context['events'] = EventModel.objects.order_by('-end_date')
        theComments=CommentModel.objects.order_by('-post')
        context['theComments']=theComments
        catigories=Categories.objects.all()
        context['catigories']=catigories
        recipes=Post.objects.order_by('-post_date')[0:5]
        context['recipes']=recipes
        featured = PostModel.objects.filter(featured=True)[0:5]
        latest = PostModel.objects.order_by('-published_on')[0:3]
        context['featured']= featured
        context['latest'] = latest
        cursor=connection.cursor()
        cursor.execute("select fdb.feedback,au.first_name,au.last_name,au.profile_photo from events_feedbackcommentmodel as fdb,accounts_user as au where fdb.userId_id=au.id;" )
        feedback_list=cursor.fetchall()
        context['feedback_list']=feedback_list
        return context

class AboutUsView(TemplateView):
    template_name="main/about-us.html"

class ContactUsView(TemplateView):
    template_name="main/contact-us.html"


