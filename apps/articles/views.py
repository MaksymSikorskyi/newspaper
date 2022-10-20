from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin, ProcessFormView

from apps.comments.forms import CommentForm

from .models import Article


class ArticleListView(ListView):
    queryset = Article.objects.filter(published_at__isnull=False).order_by(
        "-published_at"
    )
    context_object_name = "articles"


class ArticleDetailView(SuccessMessageMixin, FormMixin, DetailView, ProcessFormView):
    queryset = Article.objects.all()
    context_object_name = "article"
    form_class = CommentForm
    success_message = _("Thank you from your comment!")

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
