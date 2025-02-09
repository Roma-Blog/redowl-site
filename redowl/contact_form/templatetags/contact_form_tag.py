from django import template
from ..forms import ContactForm

register = template.Library()

@register.simple_tag
def contact_form():
    form = ContactForm()
    return {'contact_form': form}