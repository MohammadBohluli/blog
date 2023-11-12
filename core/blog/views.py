from typing import Any
from django.db import models
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Post


class PostListView(ListView):
    model = Post
    template_name = "pages/blog/post_list.html"
    queryset = Post.objects.all()
    context_object_name = "posts"


class PostDetailView(DetailView):
    model = Post
    template_name = "pages/blog/post_detail.html"
    context_object_name = "post"
    
    def get_object(self):
        return get_object_or_404(Post, id=self.kwargs.get('id'))
        

