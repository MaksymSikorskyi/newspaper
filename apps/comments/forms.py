from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Comment


class CommentForm(forms.ModelForm):
    message = forms.CharField(
        min_length=5,
        max_length=600,
        widget=forms.Textarea(
            attrs={"rows": 3, "placeholder": _("Your comment...")},
        ),
        label="",
    )

    class Meta:
        model = Comment
        fields = ["message"]
