from django import template
from ..models import Service

register = template.Library()

@register.simple_tag
def list_services():
    return Service.objects.all()