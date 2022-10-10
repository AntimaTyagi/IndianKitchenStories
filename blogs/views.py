from django.db.models import fields
from django.db.models.base import Model
from django.http import request
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView ,DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin, UpdateView
from django.views.generic.list import ListView
from .models import CommentModel, PostModel,Category
from django.contrib.auth.mixins import LoginRequiredMixin,AccessMixin
from .forms import CommentForm, PostForm
from recipes.models import Post
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login
from django.urls.base import reverse, reverse_lazy

import datetime

class AdminRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class PostCreateView( LoginRequiredMixin,AdminRequiredMixin,CreateView):
    model=PostModel
    form_class=PostForm
    template_name="blogs/post_create.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        cat=Category.objects.all()
        recipes=Post.objects.order_by('-post_date')[0:5]
        return render(request, self.template_name, {'form': form,'Category':cat,'recipes':recipes})
    def form_valid(self, form):
      form.instance.author = self.request.user

      return super().form_valid(form)

    def get_success_url(self):

      return reverse('blogs:blog-list')
    # def post(self, request, *args, **kwargs):
    #     form = PostForm(request.POST,request.FILES)
    #     if form.is_valid():
    #         instance = PostModel(image=request.FILES['image'], title=request.POST['title'],description=request.POST['description'])
    #         instance.is_published=form.cleaned_data['is_published']
    #         instance.author=request.user
    #         instance.save()

    #         return redirect('blogs:blog-details', instance.slug)


class PostUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    form_class=PostForm
    model=PostModel
    template_name="blogs/blog_edit.html"
    success_url="/blogs/"
    slug_url_kwarg = 'slug'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super(PostUpdateView, self).get_context_data(**kwargs)
        context['Category']=Category.objects.all()
        recipes=Post.objects.order_by('-post_date')[0:5]
        context['recipes']=recipes
        return context

class PostListView(ListView):
    fields=['title','description','image','published_on','author','slug', 'categories']
    template_name="blogs/blog-list.html"
    paginate_by=5
    
    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        recipes=Post.objects.order_by('-post_date')[0:5]
        context['recipes']=recipes
        return context

    def get_queryset(self):
        queryset = PostModel.objects.filter(is_published=True).order_by('-published_on','-id')
        return queryset

    
class DraftsListView(ListView):
    model=PostModel 
    fields=['title','description','image','published_on','author','slug', 'categories']
    template_name="blogs/draft_blog-list.html"
    paginate_by=5
    
    def get_context_data(self, **kwargs):
        context = super(DraftsListView, self).get_context_data(**kwargs)
        recipes=Post.objects.order_by('-post_date')[0:5]
        context['recipes']=recipes
        return context

    def get_queryset(self):
        queryset = PostModel.objects.filter(is_published=False).order_by('-published_on')
        return queryset

class PostDetailView(FormMixin,DetailView,LoginRequiredMixin):
    model=PostModel
    template_name="blogs/post_details.html"
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        the_post=PostModel.objects.get(slug=slug)
        context['comments'] = CommentModel.objects.filter(post=the_post).select_related('commenter').all()
        context['postmodel']=PostModel()
        recipes=Post.objects.order_by('-post_date')[0:5]
        context['recipes']=recipes
        return context

    def post(self, request, slug):
        post = get_object_or_404(PostModel, slug=slug)
        form = CommentModel(comment=request.POST['comment'],commenter=request.user,post=post,created_date=datetime.datetime.now())
        form.save()
        return redirect('blogs:blog-details', post.slug)

class AddCommentView(CreateView):
    model=CommentModel
    template_name="blogs/post_details.html"
    fields='__all__'

class CategoriesCreateView(CreateView):
    model=Category
    template_name="blogs/blog_categories.html"
    fields=['title']
    success_url = "/blogs/create"
    def get_context_data(self,*args, **kwargs):
        context = super(CategoriesCreateView, self).get_context_data(*args,**kwargs)
        recipes=Post.objects.order_by('-post_date')[0:5]
        context['recipes']=recipes
        return context


    


# class DeleteBlogView(LoginRequiredMixin,DesleteView):
#     model = PostModel
#     success_url = "/blogs/"
#     def get(self, request, *args, **kwargs):
#         return self.post(request, *args, **kwargs)


# class CommentListView(ListView):
#     model=CommentModel
#     fields='__all__'
#     template_name="blogs/comments.html"
#     def get_context_data(self,*args, **kwargs):
#         context = super(CommentListView, self).get_context_data(*args,**kwargs)
#         context['comments'] = CommentModel.objects.all()
#         return context





