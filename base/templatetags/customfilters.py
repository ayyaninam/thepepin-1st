# custom_filters.py
from django import template
import os

register = template.Library()

@register.filter
def basename(value):
    return os.path.basename(value)

@register.filter
def to_embed(value):
    try:
        value = value.replace("/watch","/embed")
    except:
        value = value
        
    return value
