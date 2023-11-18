from django.shortcuts import render, get_object_or_404
from .models import Post


def post_list_view(request):
    post_list = Post.objects.all()

    context = {
        'posts': post_list,
        'title': 'Blogs',
    }

    return render(request, 'pages/blog/post_list.html', context)


def post_detail_view(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        published_at__year=year,
        published_at__month=month,
        published_at__day=day,
        slug=post)
    context = {
        'post': post,
    }
    return render(request, 'pages/blog/post_detail.html', context)
        

