# -*- coding: utf-8 -*-
# Copyright (C) 2015-2016 Tim Langeman and contributors
# <see AUTHORS.txt file>
#
# This library is part of the Neotext project:
# http://www.neotext.net/

# The code for this server library is released under the MIT License:
# http://www.opensource.org/licenses/mit-license

from django.apps import AppConfig


class NeotextConfig(AppConfig):
    name = 'neotext'
    verbose_name = "Neotext Quote Context"

    # def ready(self):
    #    post_migrate.connect(do_stuff, sender=self)
