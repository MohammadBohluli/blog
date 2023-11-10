from django.contrib import admin
from .models import Post, Category


class PostAdmin(admin.ModelAdmin):
    model = Post
    list_display = [
        "author",
        "title",
    ]


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ["name"]


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
