# -*- coding: utf-8 -*-
# Copyright (C) 2015-2016 Tim Langeman and contributors
# <see AUTHORS.txt file>
#
# This library is part of the Neotext project:
# http://www.neotext.net/

# The code for this server library is released under the MIT License:
# http://www.opensource.org/licenses/mit-license

from neotext.lib.neotext_quote_context.quote_context import QuoteContext
from neotext.lib.neotext_quote_context.document import Document
from neotext.lib.neotext_quote_context.utility import Text
from neotext.settings import HASH_ALGORITHM
from bs4 import BeautifulSoup
from functools import lru_cache
from django.core.cache import cache
import hashlib
import html
import time

__author__ = 'Tim Langeman'
__email__ = "timlangeman@gmail.com"
__copyright__ = "Copyright (C) 2015-2016 Tim Langeman"
__license__ = "MIT"
__version__ = "0.2"


class Quote:
    """Looks up quote from cited url and returns the surrounding context

    * Calculates hash of: citing_url|url|quote
    * Computes text version of html
    * Calculates quote context using: QuoteContext class
        which uses google_diff_match_patch (levenshtein) algorithm
    * Returns: dictionary: context()

    Usage: Quote (
        citing_quote="one does not live by bread alone, "
        "but by every word that comes from the mouth of the Lord",
        citing_url='http://www.neotext.net/demo/',
        cited_url='https://www.biblegateway.com/passage/?search=Deuteronomy+8&amp;version=NRSV'
    )
    """

    def __init__(
        self,
        citing_quote,  # excerpt from citing document
        citing_url,    # url of the document that is doing the quoting
        cited_url,  # url of document that is being quoted
        citing_text='',   # optional: text from citing document
        citing_raw='',    # optional: raw content of citing document
        text_output=True,  # output computed text version of url's html
        raw_output=True,  # output full html/pdf source of cited url
        prior_quote_context_length=500,  # length of excerpt before quote
        after_quote_context_length=500,  # length of excerpt after quote
        starting_location_guess=None   # guess used by google diff_match_patch
    ):
        self.start_time = time.time()  # measure elapsed time
        self.citing_quote = citing_quote
        self.citing_url = citing_url
        self.cited_url = cited_url
        self.citing_text = citing_text
        self.citing_raw = citing_raw
        self.text_output = text_output
        self.raw_output = raw_output
        self.prior_quote_context_length = prior_quote_context_length
        self.after_quote_context_length = after_quote_context_length
        self.starting_location_guess = starting_location_guess

    def hash_key(self):
        """ The hash is based on a concatination of:
            citing_quote|citing_url|cited_url
        """
        return ''.join([Text(self.citing_quote).normalize(''), '|',
                        Text(self.citing_url).escape_url(), '|',
                        Text(self.cited_url).escape_url()
                        ])

    def hash(self):
        """
            Generate hash of the key, based on hash algorith (sha1)
        """
        hash_method = getattr(hashlib, HASH_ALGORITHM)
        hash_text = self.hash_key()
        return hash_method(hash_text.encode('utf-8')).hexdigest()

    def cache_key(self):
        return "quote_data_" + self.hash()

    def error(self):
        """
            If there is a problem calculating the quote context, an
            error is stored in self.data()['error']
            returns boolean
        """
        return ('error' in self.data())

    def error_str(self):
        return self.data()['error']

    @lru_cache(maxsize=50)
    def data(self, all_fields=True):
        """
            Calculate context of quotation using QuoteContext class
            Optionally return a smaller subset of fields to upload to cloud
        """
        cached_data = cache.get(self.cache_key())
        if cached_data:
            print("Returning cached Quote Data: " + self.cited_url)
            return cached_data
        else:
            print("Looking up data() for " + self.cited_url)
            data_dict = {
                'sha1': self.hash(),
                'citing_url': self.citing_url,
                'cited_url': self.cited_url,
            }

            # Get text version of document if text not passed into object
            citing_text = self.citing_text
            citing_raw = self.citing_raw
            print("Populating Document: Doc, Text, Raw")
            if (len(citing_text) == 0) or (len(citing_raw) == 0):
                citing_doc = Document(self.citing_url)
                citing_text = citing_doc.text()
                citing_raw = citing_doc.raw()
            cited_doc = Document(self.cited_url)
            print("3)----data()['text']-----")
            cited_text = cited_doc.text()
            print("End Populating")

            # if self.raw_output and citing_doc:
            #    data_dict['citing_raw'] = citing_doc.raw()
            #    data_dict['cited_raw'] = Document(self.cited_url)().raw()

            data_dict['citing_text'] = citing_text
            data_dict['cited_text'] = cited_text
            # data_dict['citing_doc_type'] = citing_doc.data()['doc_type']
            # data_dict['cited_doc_type'] = cited_doc.data()['doc_type']

            # Find context of quote from within text
            citing_context = QuoteContext(self.citing_quote, citing_text)
            cited_context = QuoteContext(self.citing_quote, cited_text)

            # Populate context fields with Document methods
            quote_context_fields = [
                'context_before', 'context_after',  # 'quote',
                'quote_length',
                'quote',
                'quote_start_position', 'quote_end_position',
                'context_start_position', 'context_end_position',
            ]
            for field in quote_context_fields:
                citing_field = ''.join(['citing_', field])
                cited_field = ''.join(['cited_', field])

                data_dict[citing_field] = citing_context.data()[field]
                data_dict[cited_field] = cited_context.data()[field]

            # Stop Elapsed Timer
            elapsed_time = time.time() - self.start_time
            data_dict['create_elapsed_time'] = format(elapsed_time, '.5f')

            if not all_fields:
                excluded_fields = [
                    'cited_raw', 'citing_raw',
                    'citing_text', 'cited_text',
                    'citing_quote_length',
                    'cited_quote_start_position',
                    'citing_quote_start_position',
                    'cited_quote_end_position',
                    'citing_quote_end_position',
                    'cited_context_start_position',
                    'citing_context_start_position',
                    'cited_context_end_position',
                    'citing_context_end_position',
                    'create_elapsed_time',
                ]  # 'cited_cache_url', 'cited_archive_url',

                for excluded_field in excluded_fields:
                    data_dict.pop(excluded_field)

            cache.set(self.cache_key(), data_dict, 60)
            return data_dict


def html_to_text(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text()


def convert_special_characters(content):
    replacement_chars = {
        '\n': " ",
        '&nbsp;': " ",
        '#8217': "'",
        u'\xa0': " "
    }
    for char in replacement_chars:
        content = content.replace('', "'")
    return content


# Non-class functions ####
def trim_encode(content):
    content = content.strip()
    content = convert_special_characters(content)
    content = html.unescape(content)
    return content
