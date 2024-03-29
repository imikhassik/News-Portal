from django.http import HttpResponse
from django.views import View
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy, reverse
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.utils.timezone import datetime
from django.core.cache import cache
from django.utils.translation import gettext as _

from .models import Post, Author, Category
from .filters import PostsFilter
from .forms import PostForm
from .resources import *
from .tasks import notify_subscribers


class Index(View):
    def get(self, request):
        string = _('Hello world')

        return HttpResponse(string)


class PostsList(ListView):
    model = Post
    ordering = '-created_on'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_of_posts'] = len(Post.objects.all())
        return context


class NewsList(ListView):
    model = Post
    queryset = Post.objects.filter(type='N')
    ordering = '-created_on'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_of_news'] = len(Post.objects.filter(type='N'))
        return context


class ArticlesList(ListView):
    model = Post
    queryset = Post.objects.filter(type='A')
    ordering = '-created_on'
    template_name = 'articles.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_of_articles'] = len(Post.objects.filter(type='A'))
        return context


class CategoriesList(ListView):
    model = Category
    queryset = Category.objects.all()
    ordering = 'name'
    template_name = 'categories.html'
    context_object_name = 'categories'


class PostsByCategory(ListView):
    model = Post
    template_name = 'posts_in_category.html'
    context_object_name = 'posts_in_category'

    def get_queryset(self):
        posts_by_category = Post.objects.filter(categories=self.kwargs['pk'])
        return posts_by_category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(pk=self.kwargs['pk'])
        context['cat'] = category
        context['subscribers'] = category.subscribers.all()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    queryset = Post.objects.all()

    def get_object(self, *args, **kwargs):
        obj = cache.get(f"post-{self.kwargs['pk']}", None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f"post-{self.kwargs['pk']}", obj)

        return obj


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


class NewsCreate(LoginRequiredMixin, CreateView, PermissionRequiredMixin):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.type = 'N'
        self.object.author = Author.objects.get(user_id=self.request.user.id)
        self.object.save()
        result = super().form_valid(form)
        notify_subscribers.apply_async([self.object.pk])
        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        context['no_more_posts'] = Post.objects.filter(
            author=Author.objects.get(user_id=self.request.user.id),
            created_on__date=datetime.date(datetime.today())).count() >= 3
        return context


class ArticlesCreate(LoginRequiredMixin,  CreateView, PermissionRequiredMixin):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'article_edit.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.type = 'A'
        self.object.author = Author.objects.get(user_id=self.request.user.id)
        self.object.save()
        result = super().form_valid(form)
        notify_subscribers.apply_async([self.object.pk])
        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        context['no_more_posts'] = Post.objects.filter(
            author=Author.objects.get(user_id=self.request.user.id),
            created_on__date=datetime.date(datetime.today())).count() >= 3
        return context


class PostUpdate(LoginRequiredMixin, UpdateView, PermissionRequiredMixin):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post

    def get_template_names(self):
        post = self.get_object()
        if post.author == self.request.user.author:
            if post.type == news and 'news' in self.request.path:
                self.template_name = 'news_edit.html'
            elif post.type == article and 'article' in self.request.path:
                self.template_name = 'article_edit.html'
            else:
                self.template_name = '404.html'
            return self.template_name
        else:
            self.template_name = 'wrong_author.html'
            return self.template_name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class PostDelete(LoginRequiredMixin, DeleteView, PermissionRequiredMixin):
    permission_required = ('news.delete_post',)
    model = Post
    success_url = reverse_lazy('posts_list')

    def get_template_names(self):
        post = self.get_object()
        if post.type == news and 'news' in self.request.path:
            self.template_name = 'news_delete.html'
        elif post.type == article and 'article' in self.request.path:
            self.template_name = 'article_delete.html'
        else:
            self.template_name = '404.html'
        return self.template_name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


def subscribe(request, pk):
    category = Category.objects.get(pk=pk)
    category.subscribers.add(request.user.id)
    return HttpResponseRedirect(reverse('posts_in_category', args=[pk]))


def unsubscribe(request, pk):
    category = Category.objects.get(pk=pk)
    category.subscribers.remove(request.user.id)
    return HttpResponseRedirect(reverse('posts_in_category', args=[pk]))
