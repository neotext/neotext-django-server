# -*- coding: utf-8 -*-
# Copyright (C) 2015-2016 Tim Langeman and contributors
# <see AUTHORS.txt file>
#
# This library is part of the Neotext project:
# http://www.neotext.net/

# The code for this server library is released under the MIT License:
# http://www.opensource.org/licenses/mit-license

from neotext.models import Quote as QuoteModel
from django.db.utils import IntegrityError
from neotext.lib.neotext_quote_context.quote import Quote as QuoteLookup
from neotext.lib.neotext_quote_context.document import Document
from bs4 import BeautifulSoup
from neotext.settings import NUM_DOWNLOAD_PROCESSES
from multiprocessing import Pool
import time
# import pdb

__author__ = 'Tim Langeman'
__email__ = "timlangeman@gmail.com"
__copyright__ = "Copyright (C) 2015-2016 Tim Langeman"
__license__ = "MIT"
__version__ = "0.2"


class URL:
    """Looks up all the quotes on a publicly-accessible page"""

    def __init__(self, url):
        self.start_time = time.time()  # measure elapsed time
        self.url = url

    def __str__(self):
        return self.url

    def raw(self):
        raw = ''
        doc = Document(self.url)
        raw = doc.raw()
        return raw

    def doc_type(self):
        return 'html'  # hard-coded

    def html(self):
        html = ''
        if (self.doc_type() == 'html'):
            html = self.raw()
        return html

    def text(self):
        text = ''
        if self.doc_type() == 'html':
            html = self.html()
            text = html.get_text()
        return text

    def citation_urls(self):
        """ Returns a dictionary of url and quote text from all
            blockquote and q tags on this page
        """
        cite_urls = {}
        soup = BeautifulSoup(self.html(), 'html.parser')
        for cite in soup.find_all(['blockquote', 'q']):
            if cite.get('cite'):
                cite_urls[cite.get('cite')] = cite.text
        return cite_urls

    def citations_list_dict(self):
        """ Create list of quote dictionaries """
        citations_list = []

        for cited_url, citing_quote in self.citation_urls().items():
            quote = {}
            quote['citing_quote'] = citing_quote
            quote['citing_url'] = cited_url
            quote['cited_url'] = self.url
            citations_list.append(quote)
        return citations_list

    def publish_citations(self, update=True):
        print("Publishing citations ..")
        update = True
        citations_data_list = self.citations(update)
        return citations_data_list

    def citations(self, update=False):
        """ Returns a list of Quote keys for all citations on this page
            Uses asycnronous pool to achieve parallel processing
        """
        result_list = []

        if update:
            quote_function = publish_quote
        else:
            quote_function = load_quote_data

        print("Looking up citations: ")
        pool = Pool(processes=NUM_DOWNLOAD_PROCESSES)

        try:
            result_list = pool.map(
                quote_function, self.citations_list_dict()
            )
        except ValueError:
            print("Skipping map value ..")

        pool.close()
        print("finished citations.")
        return result_list  # citations_data_list


def load_quote_data(quote_keys):
    """ lookup quote data, from keys """
    """
    quote_keys = {}
    quote_keys['citing_quote'] = "somewhat inspired and sweeping, but not fully baked"
    quote_keys['citing_url'] = "http://www.openpolitics.com/2016/05/13/ted-nelson-philosophy-of-hypertext/"
    quote_keys['cited_url'] = "http://www.openpolitics.com/links/philosophy-of-hypertext-ted-nelson-pg-26/"
    """
    print("Downloading: " + quote_keys['citing_url'])
    quote = QuoteLookup(
                quote_keys['citing_quote'],
                quote_keys['citing_url'],
                quote_keys['cited_url']
            )
    quote_dict = quote.data()
    print("  found: quote dict data")
    return quote_dict


def publish_quote(quote_keys):
    """ Updating db, local json, and cloud json .. """
    print("Saving model")

    filename = ''
    quote_dict = load_quote_data(quote_keys)
    print("Found data: " + quote_dict['citing_url'])
    try:
        q = QuoteModel(**quote_dict)
        q = q.save()
    except IntegrityError:
        print("  except IntegrityError")
        quote = QuoteModel.objects.filter(sha1=quote_dict['sha1'])
        q = quote.update(**quote_dict)

    # Get the record to pass on
    q = QuoteModel.objects.get(sha1=quote_dict['sha1'])

    print("  saved quote.  Does q exist?")
    try:
        print("Found q id = " + str(q.id))
        filename = q.publish_json()
        return filename

    except AttributeError:  # 'NoneType' object has no attribute 'id'
        print("    -unable to save quote. q doesn't exist")
        return ''
