from django.urls import path

from .views import (
    ArticleListView,
    ArticleDetailView,
    ArticleByCategoryListView,
    ArticleByTagListView,
)

app_name = "articles"

# article details urls possible variants:
# /<pk>/ - show by id
# /<slug>/ - show by slug
# /<year>/<month>/<day>/<slug>/ - show by slug and puublication date

urlpatterns = [
    path(
        "by-category/<slug:slug>/",
        ArticleByCategoryListView.as_view(),
        name="by-category",
    ),
    path("by-tag/<slug>/", ArticleByTagListView.as_view(), name="by-tag"),
    path(
        "<int:year>/<int:month>/<int:day>/<slug:slug>/",
        ArticleDetailView.as_view(),
        name="detail",
    ),
    path("", ArticleListView.as_view(), name="list"),  # url name: articles:list
]
