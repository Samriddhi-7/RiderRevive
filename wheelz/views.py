from django.shortcuts import render, get_object_or_404
#from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from .models import Post
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView
)

# Create your views here.

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'wheelz/home.html', context)

def about(request):
    return render(request, 'wheelz/about.html', {'title':'About'})


class PostListView(ListView):
    model = Post
    template_name = 'wheelz/home.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 3

class UserPostListView(ListView):
    model = Post
    template_name = 'wheelz/user_posts.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 3

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(publisher=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['model', 'company','details','featured_images']

    def form_valid(self, form):
        form.instance.publisher = self.request.user
        form.save()
        return super().form_valid(form)
 
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['model', 'company','featured_images','details']

    def form_valid(self, form):
        form.instance.publisher = self.request.user
        form.instance.featured_images = self.request.FILES.get('featured_images', form.instance.featured_images)

        return super().form_valid(form)
 
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.publisher:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.publisher:
            return True
        return False    