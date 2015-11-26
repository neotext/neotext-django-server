#!/usr/bin/python2.7
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

from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.db import IntegrityError, DatabaseError, ProgrammingError
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from urllib import parse
from io import open
import codecs
import os.path, json, datetime
import urllib.request
from .models import Quote
from neotext.lib.neotext_quote_context.quote import Quote as QuoteLookup
import hashlib

def index(request):
    return HttpResponse("Hello, world. \
        You're at the neotext webservice homepage.")

def demo(request):
    citing_quote = request.POST.get('citing_quote',"I was told on the phone — I forget by whom — that my good friend Roger Gregory, who was in charge at XOC down south in Palo Alto, was throwing things and acting crazy. I heard that ‘everybody was ready to leave,’ possibly quit within a day or so.")  
    citing_url = request.POST.get('citing_url',"http://www.openpolitics.com/2015/09/06/ted-nelson-philosophy-of-hypertext/")  
    cited_url = request.POST.get('cited_url',"http://www.openpolitics.com/links/possiplex-ted-nelson-pg-261/")  

    post_values = {'citing_quote' : citing_quote,
        'citing_url' : citing_url,
        'cited_url' : cited_url
    }

    #url = 'http://db.neotext.net/quote/'
    url = 'http://neotext.webfactional.com/quote/'
	
    data = parse.urlencode(post_values)
    data = data.encode('utf-8') # data should be bytes
    req = urllib.request.Request(url, data)
    with urllib.request.urlopen(req) as response:
        json = response.read()
	
    """
    citing_url = 'http://www.openpolitics.com/2015/09/06/ted-nelson-philosophy-of-hypertext/'
    cited_url = 'http://www.openpolitics.com/links/possiplex-ted-nelson-pg-261/'
    citing_quote = 'I was told on the phone — I forget by whom — that my good friend Roger Gregory, who was in charge at XOC down south in Palo Alto, was throwing things and acting crazy. I heard that ‘everybody was ready to leave,’ possibly quit within a day or so.'

    q = QuoteLookup(citing_quote, citing_url, cited_url)
    json = q.json()
    """
    return HttpResponse(json, content_type='application/json', status=201) # 201=created	
	
def quote_index_html(request, sha1):
    quote = get_object_or_404(Quote, pk=sha1)
    return render(request, 
        'quote/quote_index.html', 
        {'quote': quote, 'request_type': request.GET }
    )

@csrf_exempt
def quote_index_json(request, sha1=None):
    """ Lookup context from POSTed quote and url
    Save resulting json file to Amazon S3

    Reads should be done from amazon S3: 
    Example:  http://read.neotext.net/quote/sha1/sha1_hash
    """
    FILESYSTEM_PATH = "/home/neotext/webapps/neotext_static/quote/sha1/"
	
    data_dict = {}  # quote context data
    data = {}
    if len(request.POST) == 0:
        if not ACCEPT_READ_REQUESTS:
            return HttpResponse(status=401) # bad request
        else:
            if sha1:
                data_dict = get_quote_dict_from_sha(sha1)

                if data_dict: # test
                    data = json.dumps(data_dict)
                    return HttpResponse(data, content_type='application/json', \
                        status=201) #201=created
                else:
                    raise Http404
    else:
        citing_quote = request.POST.get('citing_quote','')  
        citing_quote = citing_quote.strip()
        citing_url = request.POST.get('citing_url','')  
        cited_url = request.POST.get('cited_url', '')

        if len(citing_quote) == 0:
            return HttpResponse(status=400) # bad request

        if ( not(is_url(citing_url)) or not(is_url(cited_url)) ):
            return HttpResponse(status=400) # bad request
		
        #Create Quote Record, By Downloading cited URL
        q = QuoteLookup(citing_quote, citing_url, cited_url)
        data_dict = q.dict()

        if 'error' in data_dict:
            raise Http404

        # Save result to database
        try:
            q = Quote(**data_dict)
            q.save()

        except (IntegrityError, DatabaseError, ProgrammingError) as e:
            return HttpResponse(status=409) # conflict

        filename = ''.join([FILESYSTEM_PATH, data_dict['sha1'],'.json'])
        #data = q.json()

        #with open(filename, 'wb') as outfile:
        #    json.dump(data, outfile, indent=4, ensure_ascii=False)

        #save_json_to_cloud(filename, filedata)
	
    #return HttpResponse(data, \
    #    content_type='application/json', status=201) # 201=created

    return HttpResponse("DB Script. \
        You're at the neotext webservice.")

def get_quote_dict_from_sha(sha1):
    try:
        quote = Quote.objects.get(sha1=sha1)
    except Quote.DoesNotExist:
        return None
		
    #Extract fields from Database record
    data_dict = {}
    opts = quote._meta
    selected_fields = ('citing_url', 'citing_quote', 
        'citing_context_before', 'citing_context_after', 'citing_doc_type',  \
        'cited_url', 'cited_quote', \
        'cited_context_before', 'cited_context_after', \
        'cited_doc_type')

    for f in opts.concrete_fields:
        if f.name in selected_fields:
            if f.name == 'created':
                data_dict[f.name] = str(f.value_from_object(quote))
            else:
                data_dict[f.name] = f.value_from_object(quote)

    return data_dict

def is_url(url_string):
    parsed_url = parse.urlparse(url_string)
    return bool(parsed_url.scheme)
	
def hashkey(cited_url, citing_url, citing_quote):
    return ''.join([ trim_encode(cited_url) , "|", 
                trim_encode(citing_url), "|", 
                trim_encode(citing_quote) 
    ]) 
def sha(cited_url, citing_url, citing_quote):
    hash_key = hashkey(cited_url, citing_url, citing_quote)
    return hashlib.md5(hash_key).hexdigest()

def trim_encode(str):
    str = str.strip()
    return str
