from django.contrib import admin

from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    date_hierarchy = "created_at"

    list_display = ("__str__", "user", "article", "created_at")
    list_filter = ("created_at",)

    search_fields = ("message",)
