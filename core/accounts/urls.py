from django.urls import path
from .views import LoginViewPage, LogoutViewPage, register_view

app_name = 'account'
urlpatterns = [
    path('login/', LoginViewPage.as_view(), name='login'),
    path('logout/', LogoutViewPage.as_view(), name='logout'),
    path('register/', register_view, name='register'),
]