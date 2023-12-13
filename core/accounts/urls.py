from django.urls import path
from . import views


app_name = "accounts"
urlpatterns = [
    path("", views.ProfileView.as_view(), name="profile"),
    # CRUD Posts
    path("create_post", views.create_post_view, name="create_post"),
    path("edit_post/<int:post_id>", views.edit_post_view, name="edit_post"),
    path("delete_post/<int:post_id>", views.delete_post_view, name="delete_post"),
    # Authentications
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("signup/", views.signup_view, name="signup"),
    path("activate/<uidb64>/<token>/", views.activate_user_view, name="activate"),
    path("password_change/", views.password_change_view, name="password_change"),
    path("password_reset/", views.password_reset_view, name="password_reset"),
    path(
        "reset/<uidb64>/<token>/",
        views.password_reset_confirm_view,
        name="password_reset_confirm",
    ),
]
