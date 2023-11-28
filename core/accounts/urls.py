from django.urls import path
from .views import LoginViewPage, LogoutViewPage
urlpatterns = [
    path('login/', LoginViewPage.as_view(), name='login'),
    path('logout/', LogoutViewPage.as_view(), name='logout'),
]