from django.shortcuts import render

# Create your views here.

def posts_list(request):
    return render(request, 'posts/posts_list.html', {})

def post_details(request):
    return render(request, 'posts/post_details.html', {})