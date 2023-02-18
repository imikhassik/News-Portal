from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView
)

from .models import Post
from .filters import PostsFilter
from .forms import PostForm
from .resources import *


class PostsList(ListView):
    model = Post
    ordering = '-created_on'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_of_news'] = len(Post.objects.all())
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostsSearch(ListView):
    model = Post
    ordering = '-created_on'
    template_name = 'posts_search.html'
    context_object_name = 'posts_search'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

    def get_initial(self):
        return {'type': news}


class ArticlesCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'article_edit.html'

    def get_initial(self):
        return {'type': article}


class NewsUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'
