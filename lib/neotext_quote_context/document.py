# -*- coding: utf-8 -*-
# Copyright (C) 2015-2016 Tim Langeman and contributors
# <see AUTHORS.txt file>
#
# This library is part of the Neotext project:
# http://www.neotext.net/

# The code for this server library is released under the MIT License:
# http://www.opensource.org/licenses/mit-license

from bs4 import BeautifulSoup
from functools import lru_cache
from django.core.cache import cache
from neotext.lib.neotext_quote_context.utility import Text
import requests
from requests.exceptions import SSLError
import base64
import hashlib
import re

import logging
logger = logging.getLogger(__name__)

__author__ = 'Tim Langeman'
__email__ = "timlangeman@gmail.com"
__copyright__ = "Copyright (C) 2015-2017 Tim Langeman"
__license__ = "MIT"
__version__ = "0.2"


class Document:
    """ Looks up url and computes plain-text version of document
        Uses caching to prevent repeated lookups

        Usage:
        doc = Document('http://www.openpolitics.com/philosophy.html')
    """

    def __init__(self, url	):
        self.url = url

    def url(self):
        return self.url

    def hex_key(self):
        url = self.url.encode('utf-8')
        key = base64.urlsafe_b64encode(hashlib.md5(url).digest())[:16]
        return key.decode('utf-8')

    def cache_key(self):
        return "document_" + self.hex_key()

    #  @lru_cache(maxsize=100)
    def raw(self):
        raw = cache.get(self.cache_key())
        if raw:
            print('Cache hit:' + self.url)
            return raw
        else:
            try:
                headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.0;'
                           ' WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
                r = requests.get(self.url, headers=headers)
                print('Downloaded ' + self.cache_key())
                raw = r.text
                cache.set(self.cache_key(), raw, 60)
                return raw

            except requests.HTTPError:
                raw = "document: HTTPError"
                cache.set(self.cache_key(), raw, 20)
                print("HTTPError: " + self.cache_key())
                return raw

            except SSLError:
                raw = "document: SSLError"
                cache.set(self.cache_key(), raw, 20)
                print("SSLError: " + self.cache_key())
                return raw

    def doc_type(self):
        """ Todo: Distinguish between html, text, .doc, and pdf"""
        # mime = magic.Magic(mime=True)
        # doc_type = mime.from_file(self.raw())
        # import magic	# https://github.com/ahupp/python-magic
        # return doc_type
        return 'html'  # hardcode to html for now

    def html(self):
        html = ""
        if self.doc_type() == 'html':
            html = self.raw()
        return html

    @lru_cache(maxsize=8)
    def text(self):
        """convert html to plaintext"""
        if self.doc_type() == 'html':
            t = Text(self.raw())
            return t.text()

        elif self.doc_type == 'pdf':
            # use: https://github.com/euske/pdfminer/
            return "not implemented"

        elif self.doc_type == 'doc':
            # https://github.com/deanmalmgren/textract
            return "not implemented"

        elif self.doc_type == 'text':
            return self.raw()

        return 'error: no doc_type'

    def canonical_url(self):
        # Credit: http://pydoc.net/Python/pageinfo/0.40/pageinfo.pageinfo/

        canonical_url = ""
        if self.doc_type() == 'html':
            soup = BeautifulSoup(self.raw(), 'html.parser')
            canonical = soup.find("link", rel="canonical")
            if canonical:
                canonical_url = canonical['href']
            else:
                # og_url = soup.find("meta", property="og:url")
                # canonical_url = og_url['content']
                canonical_url = ''
        return canonical_url

    def citation_urls(self):
        cite_urls = []
        soup = BeautifulSoup(self.html(), 'html.parser')
        for cite in soup.find_all(['blockquote', 'q']):
            if cite.get('cite'):
                cite_urls.append(cite.get('cite'))
        return cite_urls

    def citations(self):
        pass
        """
        for cited_url in self.citation_urls():

            q = Quote(
                "citing_quote",  # todo: lookup
                self.url,
                cited_url
            )
            q.save_to_db()
            q.save_json_to_cloud()
        """

    def data(self):
        data = {}
        data['doc_type'] = self.doc_type()
        data['html'] = self.html()
        data['raw'] = self.raw()
        data['text'] = self.text()
        data['canonical_url'] = self.canonical_url()
        return data

# Non-class functions #######################


def trim_encode(str):
    trimmed_str = str.strip()
    return trimmed_str


def normalize_whitespace(str):
    str = str.replace("&nbsp;", " ")
    str = str.replace(u'\xa0', u' ')
    str = str.strip()
    str = re.sub(r'\s+', ' ', str)
    return str
