from django.shortcuts import render
from django.views.generic import ListView
from .models import Post


class PostListView(ListView):
    model = Post
    template_name = "pages/blog-list.html"
    queryset = Post.objects.all()
    context_object_name = "posts"