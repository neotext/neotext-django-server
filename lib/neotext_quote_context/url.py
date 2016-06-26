# -*- coding: utf-8 -*-
# Copyright (C) 2015-2016 Tim Langeman and contributors
# <see AUTHORS.txt file>
#
# This library is part of the Neotext project:
# http://www.neotext.net/

# The code for this server library is released under the MIT License:
# http://www.opensource.org/licenses/mit-license

from neotext.lib.neotext_quote_context.quote import Quote
from neotext.lib.neotext_quote_context.document import Document
from bs4 import BeautifulSoup
from neotext.settings import NUM_DOWNLOAD_PROCESSES
from multiprocessing import Pool
import time

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

    def citations(self):
        """ Returns a list of Quote objects for all citations on this page
            Uses asycnronous pool to achieve parallel processing
        """

        citations = []
        pool = Pool(processes=NUM_DOWNLOAD_PROCESSES)

        result = pool.map_async(load_quote, self.citations_list_dict())
        while not result.ready():
            citations.append(result.get)
        pool.close()
        return citations

    def save_json_locally(self):
        for q in self.citations():
            try:
                q.save_json_locally()
            except AttributeError:  # Skip if not match found
                pass

    def save_citations_to_db(self):
        for q in self.citations():
            q.save_to_db()

    def save_citations_to_cloud(self):
        for q in self.citations():
            q.save_json_to_cloud()


def load_quote(q):
    quote = Quote(q['citing_quote'], q['citing_url'], q['cited_url'])
    print("Downloading: " + q['citing_url'])
    quote.save_json_locally()  # instantiate and call json method
