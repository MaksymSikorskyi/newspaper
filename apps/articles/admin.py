# python manage.py admin_generator articles(команда генерации админки на app)
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

# from .forms import ArticleAdminForm
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
class ArticleAdmin(SummernoteModelAdmin):
    date_hierarchy = "created_at"

    # form = ArticleAdminForm

    list_display = (
        "title",
        "category",
        "slug",
        "published_at",
        "is_featured",
        "created_at",
        "updated_at",
    )
    list_filter = ("category", "is_featured", "published_at", "created_at")

    readonly_fields = ("slug", "created_at", "updated_at")

    search_fields = ("title", "short_content", "content")

    summernote_fields = ("content",)
