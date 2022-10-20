from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Comment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("user"),
        on_delete=models.CASCADE,
        db_index=True,
    )
    article = models.ForeignKey(
        "articles.Article",
        verbose_name=_("article"),
        on_delete=models.CASCADE,
        related_name="comments",
        db_index=True,
    )
    message = models.TextField(_("comment"))
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("comment")
        verbose_name_plural = _("comments")

    def __str__(self):
        return self.message[:50]

    @property
    def user_name(self):
        return (
            self.user.get_short_name() if self.user.first_name else self.user.username
        )
