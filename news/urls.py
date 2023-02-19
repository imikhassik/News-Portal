from django.urls import path
from .views import (
    PostsList, PostDetail, PostsSearch,
    NewsCreate, ArticlesCreate,
    PostUpdate, PostDelete
)


urlpatterns = [
    path('', PostsList.as_view(), name='posts_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', PostsSearch.as_view(), name='posts_search'),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('articles/create/', ArticlesCreate.as_view(), name='article_create'),
    path('news/<int:pk>/edit/', PostUpdate.as_view(), name='news_update'),
    path('articles/<int:pk>/edit/', PostUpdate.as_view(), name='article_update'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
    path('articles/<int:pk>/delete/', PostDelete.as_view(), name='article_delete'),
]
