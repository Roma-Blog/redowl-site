from ..models import PostPage
from django import template

register = template.Library()

@register.simple_tag
def get_posts_list():
    return PostPage.objects.all().order_by('-latest_revision_created_at')