from django.db import models
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.fields import StreamField
from redowl.models import RedOwlPage
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

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


class ItemSiteMenu(MPTTModel):
    order = models.PositiveIntegerField(default=0, blank=True, null=True)
    name = models.CharField(max_length=255)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    page = GenericForeignKey('content_type', 'object_id')

    class MPTTMeta:
        order_insertion_by = ['order'] 

