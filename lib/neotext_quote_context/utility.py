# -*- coding: utf-8 -*-
# Copyright (C) 2015-2016 Tim Langeman and contributors
# <see AUTHORS.txt file>
#
# This library is part of the Neotext project:
# http://www.neotext.net/

# The code for this server library is released under the MIT License:
# http://www.opensource.org/licenses/mit-license

from bs4 import BeautifulSoup


class Text:
    """Normalizes Text into
        * text version of html
        * format that can be used by URL hashing
    """

    def __init__(self, string):
        self.input = string

    def __str__(self):
        return self.normalize()

    def text(self):
        soup = BeautifulSoup(self.input, "html.parser")
        invisible_tags = ['style', 'script', '[document]', 'head', 'title']
        for elem in soup.findAll(invisible_tags):
            elem.extract()  # remove elements: javascript, css, etc
        text = soup.get_text(separator=' ')

        # remove whitespace: https://stackoverflow.com/questions/1546226/simple-way-to-remove-multiple-spaces-in-a-string
        text = " ".join(text.split())

        """
        # Remove double spaces but retain line breaks
        text = '\n'.join(
            ' '.join(line.split()) for line in text.split('\n')
        )
        """
        return text

    def normalize(self, replace_chars=''):
        replace_text = ['\n', '’', ',', '.' , '-', ':', '/', '!', '`', '~', '^',
            ' ', '&nbsp', '\xa0'
        ]
        content = self.text()
        for txt in replace_text:
            content = content.replace(txt, replace_chars)
        return content
