from django.urls import path

from .views import become_author


urlpatterns = [
    path('upgrade/', become_author, name='upgrade')
]