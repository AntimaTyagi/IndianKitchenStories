from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import get_object_or_404, render,redirect
from django.views.generic import CreateView

from blogs.models import CommentModel
from .models import EventModel
from .models import EventModel,FeedbackCommentModel
from django.urls import reverse
from django.views.generic.list import ListView
from django.core.paginator import Paginator

def feedback_list_view_user(request,pk:int):

    feedback_list=FeedbackCommentModel.objects.filter(event_id=pk)

    #resuertUser=User.objects.get(id=pk)
    #userProfile=Profile.objects.get(user_id=resuertUser.id)
    #queryset = ImagesModel.objects.filter(user=resuertUser)
    #object_list=queryset.order_by('-updated_at')
    paginator = Paginator(feedback_list, 9) # Show 9 pics per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'events/feedback_list.html', {'page_obj': page_obj})



class EventCreateView(CreateView):
    model=EventModel
    fields=['title', 'description', 'price','image', 'start_date','end_date']
    template_name="events/event_create.html"
    def get_success_url(self,*args,**kwargs):
        return reverse("payment:payment_list" )


class EventListView(ListView):
    model=EventModel
    template_name="events/list.html"
    paginate_by=9
    context_object_name = 'page_obj'
 
    def get_context_data(self, **kwargs) :

        context_data = super(EventListView, self).get_context_data(**kwargs)
        events=EventModel.objects.order_by('title')

        context_data['events'] = events

        return context_data
# Create your views here.


class FeedbackCreateView(CreateView):
    model=FeedbackCommentModel
    fields=['event_id','feedback','userId','created_date','modified_date']
    template_name="events/feedback_create.html"
    def get_success_url(self):
        return reverse("payment:payment_list")



