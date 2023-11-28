from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django admin
    path("admin/", admin.site.urls),
    # User managements
    path('accounts/', include('django.contrib.auth.urls')),
    # Local
    path("", include("pages.urls", namespace='pages')),
    path("blog/", include("blog.urls", namespace='blog')),
]