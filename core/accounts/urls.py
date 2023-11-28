from django.urls import path
from .views import LoginViewPage, LogoutViewPage, RegisterViewPage

app_name = 'account'
urlpatterns = [
    path('login/', LoginViewPage.as_view(), name='login'),
    path('logout/', LogoutViewPage.as_view(), name='logout'),
    path('register/', RegisterViewPage.as_view(), name='register'),
]