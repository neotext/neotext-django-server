# -*- coding: utf-8 -*-
# Copyright (C) 2015-2016 Tim Langeman and contributors
# <see AUTHORS.txt file>
#
# This library is part of the Neotext project:
# http://www.neotext.net/

# The code for this server library is released under the MIT License:
# http://www.opensource.org/licenses/mit-license

from bs4 import BeautifulSoup
import html
import html2text


class Text:
    """Normalizes Text into
        * text version of html
        * format that can be used by URL hashing
    """

    def __init__(self, string):
        self.input = string

    def __str__(self):
        return self.normalize()

    def normalize(self):
        str = self.input
        str = escape_url(str)
        return escape_quote(str)


def escape_url(str):
    str = str.strip()
    str = str.replace('&nbsp', '')   # remove &nbsp;
    return str.replace('\xa0', '')   # remove encoded nbsp;


def escape_quote(str):
    str = escape_url(str)
    return escape(str)


def escape(content):
    content = html.unescape(content)
    return convert_special_characters(content)


def convert_special_characters(content):
    content = content.replace('&nbsp;', '')
    content = content.replace('\xa0', '')
    content = content.replace('\n', '')
    return content


def html_to_text(str):
    soup = BeautifulSoup(str, "html.parser")
    return soup.get_text()
