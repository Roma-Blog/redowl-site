from django.db import models
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from django.contrib.contenttypes.fields import GenericForeignKey
from wagtail.models import Page

class SocialMediaBlock(blocks.StructBlock):
    name = blocks.CharBlock()
    link = blocks.URLBlock()
    icon = ImageChooserBlock()

    panels = [
        FieldPanel('name'),
        FieldPanel('link'),
        FieldPanel('icon'),
    ]

    class Meta:
        verbose_name = "Социальная сеть"
        verbose_name_plural = "Социальные сети"

@register_setting
class SettingsSite(BaseGenericSetting):
    logo_header = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    email = models.EmailField(max_length=255, blank=True)
    phon_number = models.CharField(max_length=255, blank=True)

    social_media = StreamField([
        ('social_media', SocialMediaBlock()),
    ], blank=True)

    logo_footer = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    class Meta:
        verbose_name = "Настройки сайта"

class Menu(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(max_length=255)
    items = models.ManyToManyField('ItemMenu', related_name='menu')

    def delete(self, *args, **kwargs):
        items_to_delete = self.items.all()
        self.items.clear() 

        for item in items_to_delete:
            if item.menu.count() == 0:
                item.delete()

        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Меню"
        verbose_name_plural = "Меню"

class ItemMenu(models.Model):
    order = models.PositiveIntegerField(default=0, blank=True, null=True)
    name = models.CharField(max_length=255)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='page')

    sub_menu = models.ForeignKey('Menu', on_delete=models.CASCADE, related_name='sub_menu', null=True, blank=True)
