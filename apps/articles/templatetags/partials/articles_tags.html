from django import template
from django.db.models import Count
from taggit.models import Tag

from ..models import Article, Category

register = template.Library()


@register.simple_tag
def get_categories():
    return Category.objects.order_by("name")


@register.inclusion_tag("articles/partials/categories_list.html", takes_context=True)
def render_categories_list(context, show_all=True):
    active_category = context.get("category")

    return {
        "show_all": show_all,
        "total_articles": Article.published.count(),
        "active_category_id": (
            active_category.pk if active_category is not None else 0
        ),
        "categories": Category.objects.annotate(
            acticles_count=Count("articles")
        ).order_by("name"),
    }


@register.inclusion_tag("articles/partials/tags_list.html")
def render_tags_cloud():
    return {
        "tags": Tag.objects.all(),
    }
