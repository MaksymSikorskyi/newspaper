from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import F
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin, ProcessFormView
from taggit.models import Tag

from apps.comments.forms import CommentForm

from .models import Article, Category


class ArticleListView(ListView):
    queryset = Article.published.all()
    context_object_name = "articles"


class ArticleByCategoryListView(ListView):
    queryset = Article.published.all()
    context_object_name = "articles"

    def get_queryset(self):
        qs = super().get_queryset()

        category_slug = self.kwargs["slug"]
        qs = qs.filter(category__slug=category_slug)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["category"] = get_object_or_404(Category, slug=self.kwargs["slug"])

        return context


class ArticleByTagListView(ListView):
    queryset = Article.published.all()
    context_object_name = "articles"

    def get_queryset(self):
        qs = super().get_queryset()

        tag_slug = self.kwargs["slug"]
        qs = qs.filter(tags__slug=tag_slug)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["tag"] = get_object_or_404(Tag, slug=self.kwargs["slug"])

        return context


class ArticleDetailView(SuccessMessageMixin, FormMixin, DetailView, ProcessFormView):
    queryset = Article.objects.all()
    context_object_name = "article"
    form_class = CommentForm
    success_message = _("Thank you from your comment!")

    def increment_view_count(self):
        Article.objects.filter(
            slug=self.kwargs["slug"],
            published_at__year=self.kwargs["year"],
            published_at__month=self.kwargs["month"],
            published_at__day=self.kwargs["day"],
        ).update(view_count=F("view_count") + 1)

    def get(self, request, *args, **kwargs):
        # Not safe implementation
        # self.object.view_count += 1
        # self.object.save(update_fields=("view_count", "updated_at"))

        # Safer implementation (will increment on database level)
        self.increment_view_count()

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

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

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(
            self.get_context_data(form=form, object=self.object)
        )

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.article = self.object
        form.save()

        return super().form_valid(form)

    def get_success_url(self) -> str:
        return self.object.get_absolute_url()
