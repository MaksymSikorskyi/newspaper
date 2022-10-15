from django.views.generic import ListView

from .models import Article


class ArticleListView(ListView):
    queryset = Article.objects.filter(published_at__isnull=False).order_by(
        "-published_at"
    )
    context_object_name = "articles"
