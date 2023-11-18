from django.contrib import admin
from .models import Post, Category


class PostAdmin(admin.ModelAdmin):
    model = Post
    list_display = [
        "title",
        "author",
        "get_category",
    ]
    prepopulated_fields = {"slug": ["title"]}
    list_display_links = ['title',]

    @admin.display(description='category')
    def get_category(self,obj):
        res = [category.name for category in obj.category.all()]
        return ', '.join(res)


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ["name"]


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
