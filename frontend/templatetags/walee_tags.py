"""
Custom template tags for Walee
"""
from django import template
from django.templatetags.static import static
import os
from django.conf import settings

register = template.Library()


@register.simple_tag
def image_or_placeholder(image_name):
    """
    Returns the image path if it exists, otherwise returns the SVG placeholder
    Usage: {% image_or_placeholder 'logo.png' %}
    """
    # Check if PNG exists
    png_path = f'images/{image_name}'
    full_path = os.path.join(settings.BASE_DIR, 'frontend', 'static', png_path)
    
    if os.path.exists(full_path):
        return static(png_path)
    
    # Return SVG placeholder
    svg_name = image_name.replace('.png', '-placeholder.svg')
    return static(f'images/{svg_name}')


@register.filter
def format_currency(value, currency='XOF'):
    """
    Format a number as currency
    Usage: {{ amount|format_currency }}
    """
    try:
        amount = float(value)
        if currency == 'XOF':
            return f"{amount:,.0f} FCFA".replace(',', ' ')
        return f"{amount:,.2f} {currency}"
    except (ValueError, TypeError):
        return value


@register.filter
def format_number(value):
    """
    Format a number with thousands separator
    Usage: {{ number|format_number }}
    """
    try:
        num = int(value)
        return f"{num:,}".replace(',', ' ')
    except (ValueError, TypeError):
        return value
