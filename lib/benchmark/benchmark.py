# -*- coding: utf-8 -*-
# Copyright (C) 2015-2016 Tim Langeman and contributors
# <see AUTHORS.txt file>
#
# This library is part of the Neotext project:
# http://www.neotext.net/

# The code for this server library is released under the MIT License:
# http://www.opensource.org/licenses/mit-license

from django.http import HttpResponse
import time

__author__ = 'Tim Langeman'
__email__ = "timlangeman@gmail.com"
__copyright__ = "Copyright (C) 2015-2016 Tim Langeman"
__license__ = "MIT"
__version__ = "0.2"


def base_benchmark(request):
    start_time = time.time()
    base_simulation("http://example.com/")
    elapsed_time = "%s" % (time.time() - start_time)
    print(elapsed_time)
    return HttpResponse(elapsed_time)


def base_simulation(url):
    source_doc = document(url)
    # Lookup all citations, save and upload json to Cloud
    for citation in citations(source_doc):
        destination_doc = document(citation)
        doc_match = document_match(source_doc, destination_doc)
        save_to_db(doc_match)
        upload_json()
    return


def document(url):
    print('downloading ' + url)
    time.sleep(0.75)


def citations(doc):
    from bs4 import BeautifulSoup
    citations = []
    num_citations = 7
    print('getting list of citations ..')
    for i in range(num_citations):
        citations.append('http://www.example.com/' + str(i))
    return citations


def document_match(source_doc, destination_doc):
    from neotext.lib.google_diff_match_patch.diff_match_patch import diff_match_patch
    time.sleep(0.1)
    return "This is the first 500 characters."


def save_to_db(document_match):
    print("saving to db")
    time.sleep(0.1)


def upload_json():
    time.sleep(0.5)
