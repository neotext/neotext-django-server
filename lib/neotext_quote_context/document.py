# from neotext.lib.neotext_quote_context.quote import Quote
from bs4 import BeautifulSoup
from urllib.request import urlopen
from functools import lru_cache
import re
# import magic	# https://github.com/ahupp/python-magic

import logging
logger = logging.getLogger(__name__)

__author__ = 'timlangeman@gmail.com (Tim Langeman)'


class Document:
    """ Looks up url and computes plain-text version of document

        Usage:
        doc = Document('http://www.openpolitics.com/links/philosophy-of-hypertext-ted-nelson-pg-26/')
    """

    def __init__(self, url	):
        self.url = url

    def doc_type(self):
        """ Todo: Distinguish between html, text, .doc, and pdf"""
        # mime = magic.Magic(mime=True)
        # doc_type = mime.from_file(self.raw())
        # return doc_type
        return 'html'  # hardcode to html for now

    @lru_cache(maxsize=8)
    def raw(self):
        logger.debug('Downloading ' + self.url)
        raw = urlopen(self.url).read()
        return raw.decode('utf-8')

    def html(self):
        html = None
        if self.doc_type() == 'html':
            html = self.raw()
        return html

    @lru_cache(maxsize=8)
    def text(self):
        """convert html to plaintext"""
        text = ''

        if self.doc_type() == 'html':
            soup = BeautifulSoup(self.html(), "html.parser")
            # texts = soup.findAll(text=True)
            # visible_texts = filter(visible, texts)
            # text = ''.join(visible_texts)
            text = soup.get_text()
            text = normalize_whitespace(text)

        elif self.doc_type == 'pdf':
            # use: https://github.com/euske/pdfminer/
            text = "not implemented"

        elif self.doc_type == 'doc':
            # https://github.com/deanmalmgren/textract
            text = "not implemented"

        elif self.doc_type == 'text':
            text = self.raw()

        return text

    def data(self):
        data = {}
        data['doc_type'] = self.doc_type()
        data['html'] = self.html()
        data['raw'] = self.raw()
        data['text'] = self.text()
        return data

    def citation_urls(self):
        soup = BeautifulSoup(self.html(), 'html.parser')
        cite_urls = []

        for cite in soup.find_all('blockquote', 'q'):
            cite_urls.append(cite.get('cite'))

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

# Non-class functions #######################
def trim_encode(str):
    trimmed_str = str.strip()
    return trimmed_str


def normalize_whitespace(str):
    str = str.replace("&nbsp;", " ")
    str = str.replace("\n", "")
    str = str.replace(u'\xa0', u' ')
    str = str.strip()
    str = re.sub(r'\s+', ' ', str)
    return str


def visible(element):
    """Exclude non-visible html content from text-only version
      * Credit: http://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text
      * Profile: http://stackoverflow.com/users/230636/jbochi
    """

    return(element.parent.name in [
        'style', 'script', '[document]', 'head', 'title'
    ])
