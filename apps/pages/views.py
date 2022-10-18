from django.shortcuts import render

from apps.articles.models import Article


def index(request):
    featured_articles = Article.objects.filter(
        published_at__isnull=False, is_featured=True
    ).order_by("-published_at")[:3]

    return render(request, "pages/index.html", {"featured_articles": featured_articles})
