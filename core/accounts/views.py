from django.contrib.auth.views import LoginView, LogoutView
from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
class LoginViewPage(LoginView):
    template_name = 'registration/login_page.html'

class LogoutViewPage(LogoutView):
    template_name = 'registration/logout_page.html'

def register_view(request):

    if request.method == "POST":
    
        form = CustomUserCreationForm(request.POST)
        print('form_register', form)

        if form.is_valid():
            form.save()

            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            

            user = authenticate(email=email, password=password)
            login(request,user)
            
            return redirect('pages:home_page')
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form
    }
    return render(request, 'registration/register_page.html', context)