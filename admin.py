# -*- coding: utf-8 -*-
# Copyright (C) 2015-2016 Tim Langeman and contributors
# <see AUTHORS.txt file>
#
# This library is part of the Neotext project:
# http://www.neotext.net/

# The code for this server library is released under the MIT License:
# http://www.opensource.org/licenses/mit-license

from django.contrib import admin

# Register your models here.
from .models import Quote

__author__ = 'Tim Langeman'
__email__ = "timlangeman@gmail.com"
__copyright__ = "Copyright (C) 2015-2016 Tim Langeman"
__license__ = "MIT"
__version__ = "0.2"

class QuoteAdmin(admin.ModelAdmin):
   list_display = ('citing_url', 'citing_quote', 'cited_url')


admin.site.register(Quote, QuoteAdmin)
