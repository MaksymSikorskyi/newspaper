from django.views.generic import ListView, DetailView

from .models import Article

class ArticleListView(ListView):
    queryset = Article.objects.filter(published_at__isnull=False).order_by(
        "-published_at"
    )
    context_object_name = "articles"


class ArticleDetailView(DetailView):
    queryset = Article.objects.all()
    context_object_name = "article"

    def get_object(self, queryset=None) -> "Article":
        if queryset is None:
            queryset = self.get_queryset()

        slug = self.kwargs["slug"]
        year = self.kwargs["year"]
        month = self.kwargs["month"]
        day = self.kwargs["day"]

        return queryset.get(
            slug=slug,
            published_at__year=year,
            published_at__month=month,
            published_at__day=day,
        )
