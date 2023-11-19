from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post


def post_list_view(request):

    # querySet
    post_list = Post.objects.all()

    # handeling paginations
    paginator = Paginator(post_list, 1)
    page_number = request.GET.get('page', 1)

    try:
        post = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is string type deliver first page of results
        post = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        post = paginator.page(paginator.num_pages)


    context = {
        'posts': post,
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
        

