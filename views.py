# -*- coding: utf-8 -*-
# Copyright (C) 2015-2016 Tim Langeman and contributors
# <see AUTHORS.txt file>
#
# This library is part of the Neotext project:
# http://www.neotext.net/

# The code for this server library is released under the MIT License:
# http://www.opensource.org/licenses/mit-license

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
from neotext.lib.neotext_quote_context.url import URL
from neotext.lib.neotext_quote_context.quote import Quote as QuoteLookup
from neotext.settings import AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_S3_BUCKET, AMAZON_S3_ENDPOINT
from neotext.settings import JSON_FILE_PATH, VERSION_NUM
import tinys3
import hashlib

from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
import datetime

__author__ = 'Tim Langeman'
__email__ = "timlangeman@gmail.com"
__copyright__ = "Copyright (C) 2015-2016 Tim Langeman"
__license__ = "MIT"
__version__ = "0.2"

def index(request):
    return HttpResponse("Hello, world. \
        You're at the neotext webservice homepage.")

def post(request):
    url_post = request.POST.get('url', '')
    url = URL(url_post)
    url.save_json_locally()


    template = get_template('post.html')
    context = Context({
        'url': url,
    })
    html = template.render(context)
    return HttpResponse(html)

def demo(request):
    """
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

    citing_quote = 'The experience of writing it was one of the most intense I have ever experienced, in an exalted state of excitement and inspiration.The same epiphany I had experienced at the age of five, of the immensity and indescribability of the world, came to me again, but this time with regard to realizing how models and language and thought worked, a way of approaching the great complexity I had envisioned long before.'
    citing_url = 'http://www.openpolitics.com/2015/09/06/ted-nelson-philosophy-of-hypertext/'
    cited_url = 'http://www.openpolitics.com/links/philosophy-of-hypertext-by-ted-nelson-page-48/'

    q = QuoteLookup(citing_quote, citing_url, cited_url)
    json = q.json()
    """
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
    Example:  http://read.neotext.net/quote/sha1/v0.02/sha1_hash
    """
    ACCEPT_READ_REQUESTS = True
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
            quote = Quote(**data_dict)
            quote.save()

        except (IntegrityError, DatabaseError, ProgrammingError) as e:
            raise
            return HttpResponse(status=409) # conflict

        filename = ''.join([data_dict['sha1'],'.json'])
        local_filename = ''.join([JSON_FILE_PATH, filename])
        data = q.json()

        with open(local_filename, 'w') as outfile:
            json.dump(data, outfile, indent=4, ensure_ascii=False)

        save_json_to_cloud(filename, local_filename)

    return HttpResponse(data, \
        content_type='application/json', status=201) # 201=created

def get_quote_dict_from_sha(sha1):
    try:
        quote = Quote.objects.get(sha1=sha1)
    except Quote.DoesNotExist:
        return None

    #Extract fields from Database record
    data_dict = {}
    opts = quote._meta
    selected_fields = ('sha1', 'citing_url', 'citing_quote',
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
    return hashlib.sha1(hash_key).hexdigest()

def trim_encode(str):
    str = str.strip()
    return str


def save_json_to_cloud(filename, local_filename):
    conn = tinys3.Connection(AMAZON_ACCESS_KEY,AMAZON_SECRET_KEY,tls=True, endpoint=AMAZON_S3_ENDPOINT)
    f = open(local_filename,'rb')

    #Divide into subdirectories like git:
    #http://www.quora.com/File-Systems-Why-does-git-shard-the-objects-folder-into-256-subfolders
    shard_folder = filename[:2]
    path_list = [AMAZON_S3_BUCKET, "/quote/sha1/", VERSION_NUM, "/", shard_folder]
    bucket_folder = "".join(path_list)

    conn.upload(filename, f, bucket=bucket_folder,
        content_type='application/json'
        #expires = 'max'
    )

    print("upload succeeded.")
    return True
