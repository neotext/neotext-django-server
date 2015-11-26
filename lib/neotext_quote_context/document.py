#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

#
# Neotext Quote-Context Python Server Library
# https://github.com/neotext/neotext-quote-context-server
# 
# Copyright 2015, Tim Langeman
# http://www.openpolitics.com/tim
# 
# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT

__author__ = 'timlangeman@gmail.com (Tim Langeman)'
 
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
#import magic	# https://github.com/ahupp/python-magic

class Document:
  """ Looks up url and computes plain-text version of document

    Usage: 
    doc = Text('http://www.openpolitics.com/links/philosophy-of-hypertext-ted-nelson-pg-26/')
  """

  def __init__(self, url	):
    self.url = url

  def doc_type(self):
    """ Todo: Distinguish between html, text, .doc, and pdf"""
    #mime = magic.Magic(mime=True)
    #doc_type = mime.from_file(self.raw())
    #return doc_type
    return 'html'  #hardcode to html for now

  def raw(self):	
    raw = urlopen(self.url ).read()
    return raw.decode('utf-8')
	
  def html(self):
    html = None
    if self.doc_type() == 'html':
        html = self.raw()
    return html

  def text(self):
    """convert html to plaintext"""
    text = ''
    doc_type = self.doc_type()
		
    if doc_type == 'html': 
        soup = BeautifulSoup(self.html(), "html.parser")
        texts = soup.findAll(text=True)
        visible_texts = filter(visible, texts)
        text = ''.join(visible_texts)
        text = normalize_whitespace(text)

    elif doc_type == 'pdf':
        #use: https://github.com/euske/pdfminer/
        text = "not implemented"

    elif doc_type == 'doc':
        #https://github.com/deanmalmgren/textract
        text = "not implemented"
	
    elif doc_type == 'text':
        text = self.raw()
			
    return text	
		
  def data(self):
    data ={}
    data['doc_type'] = self.doc_type()
    data['html'] = self.html()
    data['raw'] = self.raw()
    data['text'] = self.text()
    return data
		

#### Non-class functions ####
def trim_encode(str):
  trimmed_str = str.strip()
  return trimmed_str

def normalize_whitespace(str):
    str = str.replace("&nbsp;", " ")
    str = str.replace(u'\xa0', u' ')
    str = str.strip()
    str = re.sub(r'\s+', ' ', str)
    return str

def visible(element):
    """Exclude non-visible html content from text-only version
      * Credit: http://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text
      * Profile: http://stackoverflow.com/users/230636/jbochi
    """

    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False

    return True