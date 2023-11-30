from django.contrib.auth.views import LogoutView
from .forms import CustomUserCreationForm, LoginForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


#################################
##### Login Page
#################################
def login_view(request):
    
    if request.user.is_authenticated:
        return redirect('accounts:profile')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, email=cd['email'], password=cd['password'])
            if user is not None and user.is_active:
                login(request, user)
                return redirect('accounts:profile')
            else:
                return HttpResponse("Invalid login or Your account is not active")
    else:
        form = LoginForm()

    context = {
        'form': form
    }

    return render(request, 'pages/accounts/login.html', context)


#################################
##### Logout Page
#################################
def logout_view(request):
    logout(request)
    return redirect('accounts:login')


#################################
##### Register Page
#################################
def register_view(request):

    if request.method == "POST":
    
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            form.save()

            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            
            user = authenticate(email=email, password=password)
            login(request,user)
            
            return redirect('accounts:profile')
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form
    }
    return render(request, 'registration/register_page.html', context)


#################################
##### Profile Page
#################################
@login_required
def profile_view(request):
    return render(request, 'pages/accounts/profile.html')