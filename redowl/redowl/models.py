from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel




class RedOwlPage(Page):
    '''Расширяет Wagtail Page для SEO'''
    keywords = models.TextField(blank=True)
    tag_h1 = models.TextField(blank=True)
    seo_text = RichTextField(blank=True)

    title_form = models.CharField(max_length=255, blank=True)
    text_form = models.TextField(blank=True)

    promote_panels = Page.promote_panels + [
        FieldPanel('keywords'),
        FieldPanel('tag_h1'),
        FieldPanel('seo_text'),
    ]

    class Meta:
        abstract = True
