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

    def normalize(self, replacement_chars=''):
        replace_text = ['\n', '’', ',', '.' , '-', ':', '/', '!', '`', '~', '^',
			' ', '&nbsp', '\xa0', '&#8217;', '&#169;', '&copy;', '&#174;',
			'&reg;', '&#8364;', '&euro;', '&#8482;', '&trade;',
			'&lsquo;', '&rsquo;', '&sbquo;', '&ldquo;', '&rdquo;', '&bdquo;',
			'&#34;', '&quot;', '&#38;', '&amp;', '&#39;', '&#163;', '&pound;',
			'&#165;', '&yen;', '&#168;', '&uml;', '&die;', '&#169;', '&copy;'
        ]
        content = self.text()
        for txt in replace_text:
            content = content.replace(txt, replacement_chars)
        return content

    def escape_url(self):
        # Remove leading and trailing whitespace
        return self.input.strip()
