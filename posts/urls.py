from django.urls import path

from . import views

urlpatterns = [
    path("", views.posts_lists, name="posts_lists"),
]