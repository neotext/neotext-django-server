# -*- coding: utf-8 -*-
# Copyright (C) 2015-2016 Tim Langeman and contributors
# <see AUTHORS.txt file>
#
# This library is part of the Neotext project:
# http://www.neotext.net/

# The code for this server library is released under the MIT License:
# http://www.opensource.org/licenses/mit-license

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views

__author__ = 'Tim Langeman'
__email__ = "timlangeman@gmail.com"
__copyright__ = "Copyright (C) 2015-2016 Tim Langeman"
__license__ = "MIT"
__version__ = "0.2"


urlpatterns = patterns(
    '',
    url(r'^post/', views.index, name='index'),
    url(r'^$', views.post_url, name='post_url'),
    url(r'^$url/(?P<url>\d+)/$', views.url_quotes, name='url_quotes'),
    url(r'^url/(?P<url>(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)$',
        views.url_quotes, name='url_quotes'),
    url(r'^quote/sha1/(?P<sha1>[a-fA-F\d]{40})$',
        views.quote, name='quote'),
    url(r'^quote/sha1/(?P<sha1>[a-fA-F\d]{40}).json$',
        views.quote_json, name='quote_json'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^demo/$', views.demo, name='demo'),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
