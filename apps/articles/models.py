from django.db import models
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
    title = models.CharField(_("title"), max_length=200)
    slug = AutoSlugField(
        populate_from="title", slugify_function=slugify, unique_for_date="published_at"
    )
    published_at = models.DateField(
        _("published at"), db_index=True, blank=True, null=True
    )
    short_content = models.TextField(_("short content"), max_length=600)
    content = models.TextField(_("content"))
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    tags = TaggableManager()

    main_image_thumbnail = ImageSpecField(
        source="main_image",
        processors=[ResizeToFill(450, 300)],
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