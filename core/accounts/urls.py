from django.urls import path
from .views import (
    login_view,
    profile_view,
    logout_view,
    signup_view,
    activate_user_view,
    password_change_view,
    password_reset_view,
    password_reset_confirm_view,
)

app_name = 'accounts'
urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup_view, name='signup'),
    path('', profile_view, name='profile'),
    path('activate/<uidb64>/<token>/', activate_user_view, name='activate'),
    path('password_change/', password_change_view, name='password_change'),
    path('password_reset/', password_reset_view, name='password_reset'),
    path('reset/<uidb64>/<token>/', password_reset_confirm_view, name='password_reset_confirm'),
]