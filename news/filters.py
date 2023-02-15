from django_filters import FilterSet
from .models import Post


class PostsFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'author__user': ['exact'],
            'created_on': ['gt']
        }
