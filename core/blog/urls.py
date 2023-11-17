from django.urls import path
from . import views

app_name = "blog"
urlpatterns = [
    path("", views.post_list_view, name="post_list"),
    path("<int:id>/", views.post_detail_view, name="post_detail"),
]
