from django.shortcuts import render, get_object_or_404
from .models import Post


def post_list_view(request):
    post_list = Post.objects.all()

    context = {
        'posts': post_list,
        'title': 'Posts',
    }

    return render(request, 'pages/blog/post_list.html', context)


def post_detail_view(request, id):
    # post = get_object_or_404(Post,id=id)
    post = Post.objects.get(id=id)
    context = {
        'post': post,
    }
    return render(request, 'pages/blog/post_detail.html', context)
        

