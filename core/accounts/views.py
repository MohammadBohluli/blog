from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from .forms import CustomUserCreationForm
class LoginViewPage(LoginView):
    template_name = 'registration/login_page.html'

class LogoutViewPage(LogoutView):
    template_name = 'registration/logout_page.html'

class RegisterViewPage(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('account:login')
    template_name = 'registration/register_page.html'