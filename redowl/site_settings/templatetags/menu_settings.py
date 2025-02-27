from django import template


register = template.Library()


@register.inclusion_tag('site_settings/list_pages.html')
def get_list_pages(list_pages):
    return {'list_page':list_pages}