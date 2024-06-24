from django.shortcuts import render
from .models import Post
# Create your views here.

def posts_list(request):
    return render(request, 'posts/posts_list.html', {"posts": Post.objects.all()})

def post_details(request, id):
    post = Post.objects.get(id=id)
    return render(request, 'posts/post_details.html', {"post": post})