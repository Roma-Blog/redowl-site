from wagtail.fields import RichTextField
from django.db import models
from wagtail.models import Page
from redowl.models import RedOwlPage
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel

class BlogPage(RedOwlPage):
    class Meta:
        verbose_name = "Список статей блога"
        verbose_name_plural = "Списки статей блога"

class PostPage(RedOwlPage):

    img_post = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    text_post = RichTextField(blank=True)

    content_panels = RedOwlPage.content_panels + [
        FieldPanel('img_post'),
        FieldPanel('text_post'),
    ]

    class Meta:
        verbose_name = "Страница поста"
        verbose_name_plural = "Страницы поста"