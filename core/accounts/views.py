from django.contrib.auth.views import LoginView

class LoginViewPage(LoginView):
    template_name = 'registration/login_page.html'