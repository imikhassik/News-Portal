from django.urls import path
from .views import PostsList


urlpatterns = [
    path('', PostsList.as_view()),
]
