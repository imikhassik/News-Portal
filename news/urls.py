from django.urls import path
from django.views.decorators.cache import cache_page

from .views import (
    PostsList, NewsList, ArticlesList, PostDetail, PostsSearch,
    NewsCreate, ArticlesCreate, PostUpdate, PostDelete,
    CategoriesList, PostsByCategory, subscribe, unsubscribe
)


urlpatterns = [
    path('', cache_page(60)(PostsList.as_view()), name='posts_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', PostsSearch.as_view(), name='posts_search'),
    path('news/', cache_page(60 * 5)(NewsList.as_view()), name='news_list'),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', PostUpdate.as_view(), name='news_update'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
    path('articles/', ArticlesList.as_view(), name='articles_list'),
    path('articles/create/', ArticlesCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', PostUpdate.as_view(), name='article_update'),
    path('articles/<int:pk>/delete/', PostDelete.as_view(), name='article_delete'),
    path('categories/', CategoriesList.as_view(), name='categories'),
    path('categories/<int:pk>/', PostsByCategory.as_view(), name='posts_in_category'),
    path('categories/<int:pk>/subscribe/', subscribe, name='subscribe'),
    path('categories/<int:pk>/unsubscribe/', unsubscribe, name='unsubscribe'),
]
