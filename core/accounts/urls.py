from django.urls import path
from .views import LoginViewPage
urlpatterns = [
    path('login/', LoginViewPage.as_view(), name='login'),
]