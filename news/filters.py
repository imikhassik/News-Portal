from django_filters import FilterSet, DateTimeFilter
from django import forms

from .models import Post


class PostsFilter(FilterSet):
    created_on = DateTimeFilter(
        widget=forms.DateInput(attrs={'type': 'date'}),
        lookup_expr='date__gt',
    )

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'author': ['exact'],
            'categories': ['exact']
        }
