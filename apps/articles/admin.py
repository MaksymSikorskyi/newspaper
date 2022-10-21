# python manage.py admin_generator articles(команда генерации админки на app)
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Category, Article, ArticleImage


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


class ArticleImageInline(admin.TabularInline):
    model = ArticleImage

    extra = 1


@admin.register(Article)
class ArticleAdmin(SummernoteModelAdmin):
    date_hierarchy = "created_at"

    list_display = (
        "title",
        "category",
        "slug",
        "published_at",
        "is_featured",
        "view_count",
        "created_at",
    )
    list_filter = ("category", "is_featured", "published_at", "created_at")
    readonly_fields = ("slug", "created_at", "updated_at")
    search_fields = ("title", "short_content", "content")

    summernote_fields = ("content",)

    inlines = [
        ArticleImageInline,
    ]


@admin.register(ArticleImage)
class ArticleImageAdmin(admin.ModelAdmin):
    list_display = ("article", "__str__", "created_at")
    list_display_links = ("__str__",)
    list_filter = ("created_at",)
