# -*- coding: utf-8 -*-
# Copyright (C) 2015-2016 Tim Langeman and contributors
# <see AUTHORS.txt file>
#
# This library is part of the Neotext project:
# http://www.neotext.net/

# The code for this server library is released under the MIT License:
# http://www.opensource.org/licenses/mit-license


from neotext.models import Quote as QuoteModel
from neotext.lib.neotext_quote_context.quote import Quote as QuoteLookup
from neotext.lib.neotext_quote_context.document import Document
from bs4 import BeautifulSoup
from neotext.settings import NUM_DOWNLOAD_PROCESSES
from multiprocessing import Pool
from django.core.cache import cache
from functools import lru_cache
import time

__author__ = 'Tim Langeman'
__email__ = "timlangeman@gmail.com"
__copyright__ = "Copyright (C) 2015-2017 Tim Langeman"
__license__ = "MIT"
__version__ = "0.2"


class URL:
    """Looks up all the quotes on a publicly-accessible page"""

    def __init__(self, url):
        self.start_time = time.time()  # measure elapsed time
        self.url = url

    def __str__(self):
        return self.url

    # Document methods imported here so class can make only 1 request per URL
    @lru_cache(maxsize=50)
    def doc(self):
        cache_key = "url_" + self.url
        cache_doc = cache.get(cache_key)
        if cache_doc:
            print("Cache hit: URL: " + self.url)
            doc = cache_doc
        else:
            doc = Document(self.url)
            cache.set(cache_key, doc, 60)
        return doc

    @lru_cache(maxsize=50)
    def raw(self):
        return self.doc().raw()

    def doc_type(self):
        return 'html'  # hard-coded.  Todo: pdf, text

    def html(self):
        html = ''
        if (self.doc_type() == 'html'):
            html = self.raw()
        return html

    @lru_cache(maxsize=50)
    def text(self):
        print("URL: text(self)")
        return self.doc().text()

    def citation_urls(self):
        """ Returns a dictionary of url and quote text for all
            blockquote and q tags on this page
        """
        print("Getting URLs")
        cite_urls = {}
        soup = BeautifulSoup(self.html(), 'html.parser')
        for cite in soup.find_all(['blockquote', 'q']):
            if cite.get('cite'):
                cite_urls[cite.get('cite')] = cite.text
        return cite_urls

    def citations_list(self):
        """ Create list of quote dictionaries """
        citations_list = []
        for cited_url, citing_quote in self.citation_urls().items():
            quote = {}
            quote['citing_quote'] = citing_quote
            quote['citing_url'] = self.url
            quote['citing_text'] = self.text()
            quote['citing_raw'] = self.raw()
            quote['cited_url'] = cited_url
            citations_list.append(quote)
        return citations_list

    def publish_citations(self):
        """ Save quote data to database and publish json """
        print("Publishing citations ..")
        if not self.citations():
            print('not self.citations()')
            return
        for num, quote_dict in enumerate(self.citations()):
            print("Quote: " + str(num))

            if not quote_dict:
                print("No quote_dict in self.citations()")
            else:
                sha1 = quote_dict['sha1']
                quote_dict_defaults = quote_dict
                quote_dict_defaults.pop('sha1')  # remove sha1 key
                q, created = QuoteModel.objects.update_or_create(
                    sha1=sha1,
                    defaults=quote_dict_defaults
                )
                try:
                    if q:
                        q.publish_json()
                    else:
                        print("Unable to publish: " + quote_dict['cited_url'])
                except ValueError:
                    print("Error publishing: " + quote_dict['cited_url'])
                print("Published: " + quote_dict['cited_url'])
                print("\n  SHA1=" + sha1)

    def citations(self):
        """ Returns a list of Quote Lookup results for all citations on this page
            Uses asycnronous pool to achieve parallel processing
            calls 'load_quote_data' function
            for all values in self.citations_list
            using python 'map' function
        """
        result_list = []
        citations_list = self.citations_list()
        print("Looking up citations: ")

        pool = Pool(processes=NUM_DOWNLOAD_PROCESSES)
        try:
            for quote_keys in citations_list:
                result_list = pool.map(load_quote_data, citations_list)

        except ValueError:
            print("Skipping map value ..")

        return result_list

        """
        # gevent version:

        result_list_values = [gevent.spawn(load_quote_data, **quote_keys)
                              for quote_keys in self.citations_list()
                              ]
        gevent.joinall(result_list_values)
        # Gevent results are accessed with .value   Package as list.
        for result in result_list_values:
            result_list.append(result.value)
        return result_list
        """


# @lru_cache(maxsize=25)
def load_quote_data(quote_keys):
    """ lookup quote data, from keys """
    print("Downloading citation from: " + quote_keys['cited_url'])
    # print("  Downloading: " + quote_keys['citing_quote'])
    quote = QuoteLookup(
                 quote_keys['citing_quote'],
                 quote_keys['citing_url'],
                 quote_keys['cited_url'],
                 quote_keys['citing_text'],  # optional: caching
                 quote_keys['citing_raw'],   # optional: caching
             )
    return quote.data()
