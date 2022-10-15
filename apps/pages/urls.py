from .views import index

from django.urls import path

app_name = "pages"

urlpatterns = [
    path("", index, name="index")   # URL name pages:index
]
