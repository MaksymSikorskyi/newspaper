from django.shortcuts import render

from apps.articles.models import Article


def index(request):
    featured_articles = Article.published.filter(is_featured=True)[:3]

    latest_articles = Article.published.all()[:5]

    return render(
        request,
        "pages/index.html",
        {"featured_articles": featured_articles, "latest_articles": latest_articles},
    )
