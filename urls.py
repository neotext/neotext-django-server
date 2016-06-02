#!/usr/bin/python3.4
# -*- coding: utf-8 -*-
#
# Neotext Quote-Context Python Server Library
# https://github.com/neotext/neotext-quote-context-server
# 
# Copyright 2015, Tim Langeman
# http://www.openpolitics.com/tim
# 
# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT

__author__ = 'timlangeman@gmail.com (Tim Langeman)'

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.index, name='index'),
    url(r'^quote/$', views.quote_index_json, name='quote_demo'),
    url(r'^quote/sha1/(?P<sha1>[a-fA-F\d]{40}).json$', views.quote_index_json, name='quote_index_json'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^demo/$', views.demo, name='demo'),

) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
