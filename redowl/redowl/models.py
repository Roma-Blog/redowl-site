from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel


class RedOwlPage(Page):
    '''Расширяет Wagtail Page для SEO'''
    keywords = models.TextField(blank=True)
    tag_h1 = models.TextField(blank=True)
    seo_text = RichTextField(blank=True)

    #Заголовок и текст формы в подвале, не добавля.тся сразу в настройки админки. В ручную чтобы соблюсти логический порядок настроек. 
    title_form = models.CharField(max_length=255, blank=True)
    text_form = models.TextField(blank=True)

    date_published = models.DateTimeField(auto_now_add=True)

    promote_panels = Page.promote_panels + [
        FieldPanel('keywords'),
        FieldPanel('tag_h1'),
        FieldPanel('seo_text'),
    ]

    #Получаем родительский url
    def get_perent_url(self):
        parent_page = self.get_parent()
        return parent_page.url if parent_page else None

    class Meta:
        abstract = True


