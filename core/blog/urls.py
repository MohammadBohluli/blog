from django.urls import path, re_path
from . import views

app_name = "blog"
urlpatterns = [
    path("", views.post_list_view, name="post_list"),
    
    re_path(r"post/(?P<post>[-\w]+)/$", views.post_detail_view, name='post_detail'),
    path('post/<int:post_id>/share/', views.post_share_view, name='post_share'),
    path('post/<int:post_id>/comment/', views.post_comment, name='post_comment'),
]