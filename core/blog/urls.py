from django.urls import path
from . import views

app_name = "blog"
urlpatterns = [
    path("", views.post_list_view, name="post_list"),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail_view, name='post_detail'),
    path('<int:post_id>/share/', views.post_share_view, name='post_share')
]
