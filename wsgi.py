import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'neotext.settings'

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
