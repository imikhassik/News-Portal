from django.views.generic import ListView, DetailView
from .models import Post


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
