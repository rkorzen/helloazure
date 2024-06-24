from django.urls import path

from . import views

urlpatterns = [
    path("", views.posts_list, name="posts_lists"),
    path("<int:id>/", views.post_details, name="post_details"),
]