from django.urls import path

from . import views

urlpatterns = [
    path("", views.posts_list, name="posts_lists"),
]