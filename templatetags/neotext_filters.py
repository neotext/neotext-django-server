from django import template
from datetime import date, timedelta
from urllib.parse import urlparse

register = template.Library()


@register.filter(name='get_url_domain')
def get_url_domain(url):
    u = urlparse(url)
    return u.netloc
