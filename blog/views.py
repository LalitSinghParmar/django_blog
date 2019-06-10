from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView 
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from .models import Post
# Create your views here.
# This is the Post view created using function view

def home(request):
    context = {
        'posts':Post.objects.all(),
    }
    return render(request, 'blog/home.html', context)

# This is the Post view created using class view. It will list all posts
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # By default it will expect templates like <app-name>/<model>_<viewtype>.html. 
    context_object_name = 'posts'   # By default will be <object_list> instead of posts. Since we have used posts in template, so we are changing it.
    #ordering = ['-date_posted']  # - sign to reverse the order i.e. newer first. By default older first
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # By default it will expect templates like <app-name>/<model>_<viewtype>.html. 
    context_object_name = 'posts'   # By default will be <object_list> instead of posts. Since we have used posts in template, so we are changing it.
    #ordering = ['-date_posted']  # - sign to reverse the order i.e. newer first. By default older first
    paginate_by = 5 

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post
    # Here we are not defining template_name. So by default it will take 'blog/post_detail.html' that we will create.

class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title','content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title','content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if post.author == self.request.user:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    # TBD - Try to remove duplicate code to follow DRY .
    def test_func(self):
        post = self.get_object()
        if post.author == self.request.user:
            return True
        return False

def about(request):
    return render(request, 'blog/about.html', {'title':'About'})

