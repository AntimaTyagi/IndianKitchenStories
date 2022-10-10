from django.contrib.auth.mixins import AccessMixin
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.urls.base import reverse, reverse_lazy
from django.views.generic import ListView, DetailView,CreateView

from blogs.models import Category
from .models import Post, Categories
from django.db.models import Q, fields
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseNotFound, Http404
class AdminRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
# Create your views here.
class RecipeView(ListView):
   model = Post
   template_name = 'recipes/recipe_list.html'
   cats = Categories.objects.all()
   context_object_name = "latestpost_list"
   ordering = ['-post_date']  
   paginate_by = 6

   def get_context_data(self, *args, **kwargs):
      cat_list = Categories.objects.all()
      context = super(RecipeView, self).get_context_data(*args, **kwargs)
      context["cat_list"] = cat_list
      recipes=Post.objects.order_by('-post_date')[0:5]
      context['recipes']=recipes
      return context

def search(request):
   template = 'recipes/search_list.html'
   query = request.GET.get('q')
   if query:
      posts = Post.objects.filter(Q(title__icontains=query) | Q(body__icontains=query)).order_by('-post_date')
   else:
      posts = Post.objects.all()
   
   cat_list = Categories.objects.all()
   latestpost_list = Post.objects.all().order_by('-post_date')[:3]
   paginator = Paginator(posts, 2)
   page = request.GET.get('page')
   posts = paginator.get_page(page)
   return render(request, template, {'posts':posts, 'cat_list': cat_list, 'latestpost_list':latestpost_list, 'query':query})

def categoryView(request, cats):
   if Categories.objects.filter(categoryname=cats).exists():
      category_posts = Post.objects.filter(category__categoryname=cats).order_by('-post_date')
      cat_list = Categories.objects.all()
      latestpost_list = Post.objects.all().order_by('-post_date')[:3]
      paginator = Paginator(category_posts, 6)
      page = request.GET.get('page_obj')
      category_posts = paginator.get_page(page)
      return render(request, 'recipes/recipes_in_category_list.html', {'cats':cats, 'category_posts':category_posts, 'cat_list': cat_list, 'latestpost_list':latestpost_list})
   else:
      raise Http404






class recipedetail(DetailView):
   model = Post
   template_name = 'recipes/recipe_detail.html'

   def get_context_data(self, *args, **kwargs):
      cat_list = Categories.objects.all()
      latestpost_list = Post.objects.all().order_by('-post_date')[:3]
      context = super(recipedetail, self).get_context_data(*args, **kwargs)
      context["cat_list"] = cat_list
      context["latestpost_list"] = latestpost_list
      return context

class RecipeCreateView(AdminRequiredMixin,CreateView):
   template_name="recipes/recipe_create.html"

   model=Post
   fields = [
        'title',
        'img',
        'body',
        'ingredients',
        'category',
    ]
   def get_success_url(self):
      return reverse('recipes:recipe')

   def form_valid(self, form):
      form.instance.author = self.request.user
      return super().form_valid(form)


class CategoryListView(ListView):
   model=Categories
   fields='all'
   template_name="category-list.html"
   paginate_by=9
