from django.db import models

from wagtail import blocks
from wagtail.models import Page
from redowl.models import RedOwlPage
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.fields import StreamField



class StepsWork(blocks.StructBlock):
    title = blocks.CharBlock(max_length=255)
    description = blocks.TextBlock(max_length=640)

    panels = [
        FieldPanel('title'),
        FieldPanel('description'),
    ]

    class Meta:
        verbose_name = "Этап работы"
        verbose_name_plural = "Этапы работы"

class Price(blocks.StructBlock):
    title = blocks.CharBlock(max_length=255)
    description = blocks.RichTextBlock()
    price = blocks.IntegerBlock()

    panels = [
        FieldPanel('title'),
        FieldPanel('description'),
        FieldPanel('price'),
    ]

    class Meta:
        verbose_name = "Цена"
        verbose_name_plural = "Цены"

class FaqService(blocks.StructBlock):
    question = blocks.TextBlock(max_length=400)
    answer = blocks.RichTextBlock()

    panels = [
        FieldPanel('question'),
        FieldPanel('answer'),
    ]

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

class PageServices(RedOwlPage):

    content_panels =  RedOwlPage.content_panels + [
        FieldPanel('title_form'),
        FieldPanel('text_form'),
    ]
    class Meta:
        verbose_name = "Список услуг"
        verbose_name_plural = "Списки услуг"


class Service(RedOwlPage):
    img_icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    img_template = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    anatation = models.TextField(blank=True)
    text_btn = models.CharField(max_length=96, blank=True)

    img_steps_work = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    steps_works = StreamField([
        ('steps_work', StepsWork()),
    ], blank=True)

    price_list = StreamField([
        ('price', Price()),
    ], blank=True)

    faq = StreamField([
        ('faq_service', FaqService()),
    ], blank=True)

    content_panels =  RedOwlPage.content_panels + [
        FieldPanel('img_icon'),
        FieldPanel('img_template'),
        FieldPanel('anatation'),
        FieldPanel('text_btn'),
        FieldPanel('img_steps_work'),
        FieldPanel('steps_works'),
        FieldPanel('price_list'),
        FieldPanel('faq'),
        FieldPanel('title_form'),
        FieldPanel('text_form'),
    ]

    class Meta:
        verbose_name = "Страница услуги"
        verbose_name_plural = "Страницы услуг"
