from django.views.generic import ListView, DetailView
from .models import Post


class PostsList(ListView):
    model = Post
    ordering = '-created_on'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 1


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
