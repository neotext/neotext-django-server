from django import template
from urllib.parse import urlparse

register = template.Library()


@register.filter(name='get_url_domain')
def get_url_domain(url):
    u = urlparse(url)
    return u.netloc


@register.filter(name='get_url_path')
def get_url_path(url):
    u = urlparse(url)
    return u.path


@register.filter(name='get_url_strip_protocol')
def get_url_strip_protocol(url):
    u = urlparse(url)
    return u.netloc + u.path
