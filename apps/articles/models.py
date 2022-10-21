from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_extensions.db.fields import AutoSlugField
from slugify import slugify
from taggit.managers import TaggableManager
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class Category(models.Model):
    name = models.CharField(_("name"), max_length=100)
    slug = AutoSlugField(populate_from="name", unique=True, slugify_function=slugify)
    image = models.ImageField(
        _("image"), max_length=300, upload_to="categories/images", blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("name",)
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return "<Category id={} name={} slug={} created_at={}>".format(
            self.pk, self.name, self.slug, self.created_at
        )

    def get_absolute_url(self):
        return reverse("articles:by-category", kwargs={"slug": self.slug})


class PublishedArticlesManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(published_at__isnull=False)
            .order_by("-published_at")
        )


class Article(models.Model):
    category = models.ForeignKey(
        Category,
        verbose_name=_("category"),
        on_delete=models.RESTRICT,
        db_index=True,
        related_name="articles",
    )
    main_image = models.ImageField(
        _("main image"),
        max_length=300,
        blank=True,
        null=True,
        upload_to="articles/images/%Y/%m",
    )
    is_featured = models.BooleanField(_("is featured"), default=False, db_index=True)
    title = models.CharField(_("title"), max_length=200)
    slug = AutoSlugField(
        populate_from="title", slugify_function=slugify, unique_for_date="published_at"
    )
    published_at = models.DateField(
        _("published at"), db_index=True, blank=True, null=True
    )
    short_content = models.TextField(_("short content"), max_length=600)
    content = models.TextField(_("content"))
    view_count = models.PositiveIntegerField(_("view count"), default=0, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    tags = TaggableManager()
    objects = models.Manager()
    published = PublishedArticlesManager()
    main_image_thumbnail = ImageSpecField(
        source="main_image",
        processors=[ResizeToFill(450, 300)],
        format="JPEG",
        options={"quality": 80},
    )
    main_image_medium = ImageSpecField(
        source="main_image",
        processors=[ResizeToFill(640, 480)],
        format="JPEG",
        options={"quality": 80},
    )

    class Meta:
        verbose_name = _("article")
        verbose_name_plural = _("articles")

    def __str__(self) -> str:
        return self.title

    def __repr__(self) -> str:
        return "<Article id={} title={} published_at={} created_at={}>".format(
            self.pk, self.title, self.published_at, self.created_at
        )

    @property
    def has_images(self):
        return self.images.count() > 0

    @property
    def comments_count(self):
        return self.comments.count()

    def get_comments(self):
        return self.comments.order_by("-created_at")

    def get_absolute_url(self):
        if self.published_at is None:
            return reverse("articles:list")
        return reverse(
            "articles:detail",
            kwargs={
                "slug": self.slug,
                "year": self.published_at.year,
                "month": self.published_at.month,
                "day": self.published_at.day,
            },
        )


class ArticleImage(models.Model):
    article = models.ForeignKey(
        Article,
        verbose_name=_("article"),
        on_delete=models.CASCADE,
        db_index=True,
        related_name="images",
    )
    title = models.CharField(_("title"), max_length=100, blank=True, null=True)
    image = models.ImageField(
        _("image"),
        max_length=300,
        upload_to="articles/images/%Y/%m",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image_thumbnail = ImageSpecField(
        source="image",
        processors=[ResizeToFill(450, 300)],
        format="JPEG",
        options={"quality": 80},
    )

    class Meta:
        verbose_name = _("article image")
        verbose_name_plural = _("article images")

    def __str__(self) -> str:
        return self.title if self.title else f"Article image #{self.pk}"

    def __repr__(self) -> str:
        return "<ArticleImage id={} article={} image={} created_at={}>".format(
            self.pk, self.article_id, self.image, self.created_at
        )
