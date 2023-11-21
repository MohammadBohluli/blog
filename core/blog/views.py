from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Post
from .forms import EmailPostForm
from django.core.mail import send_mail

def post_list_view(request):

    # querySet
    post_list = Post.objects.all()

    # handeling paginations
    paginator = Paginator(post_list, 5)
    page_number = request.GET.get('page', 1)

    post = paginator.get_page(page_number)


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
        

def post_share_view(request, post_id):
    post = get_object_or_404(Post, id=post_id,status=Post.Status.PUBLISHED)

    # use the sent variable in the template to display 
    # a success message when the form is successfully submitted
    is_sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f" recommends you read {post.title}"
            message = f"Read {post.title} at {post_url} {cd['name']}s comment: {cd['comment']}"

            send_mail(subject, message, 'your_account@gmail.com',[cd['to']])
            is_sent = True
    else:
        form = EmailPostForm()

    context = {
        'post': post,
        'form': form,
        'is_sent': is_sent,
    }

    return render(request, 'pages/blog/post_share.html', context)
