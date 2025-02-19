from ..models import PostPage
from django import template

register = template.Library()

@register.simple_tag
def get_posts_list(count=None):
    return PostPage.objects.all().order_by('-date_published')[:count]