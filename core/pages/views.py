from django.shortcuts import render


def home_page_view(request):
    context = {
        'title': 'Home'
    }
    return render(request,'pages/home.html',context)


def about_page_view(request):
    context = {
        'title': 'About'
    }
    return render(request,'pages/about.html',context)
