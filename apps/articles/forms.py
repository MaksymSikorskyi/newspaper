from django import forms
from django_summernote.widgets import SummernoteInplaceWidget


class ArticleAdminForm(forms.ModelForm):
    content = forms.CharField(widget=SummernoteInplaceWidget())
