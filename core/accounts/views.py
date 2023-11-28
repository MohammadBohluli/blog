from django.contrib.auth.views import LoginView, LogoutView

class LoginViewPage(LoginView):
    template_name = 'registration/login_page.html'

class LogoutViewPage(LogoutView):
    template_name = 'registration/logout_page.html'