# python manage.py admin_generator articles(команда генерации админки на app)
from django.contrib import admin

from .models import Category, Article


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "created_at",
        "updated_at",
    )
    list_filter = ("created_at",)

    readonly_fields = ("slug", "created_at", "updated_at")

    search_fields = ("name", "slug")


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "slug",
        "published_at",
        "created_at",
        "updated_at",
    )

    list_filter = ("category", "published_at", "created_at")

    readonly_fields = ("slug", "created_at", "updated_at")

    search_fields = ("title", "short_content", "content")
