# -*- coding: utf-8 -*-
# Copyright (C) 2015-2016 Tim Langeman and contributors
# <see AUTHORS.txt file>
#
# This library is part of the Neotext project:
# http://www.neotext.net/

# The code for this server library is released under the MIT License:
# http://www.opensource.org/licenses/mit-license

from django.db import models
from neotext import settings
from urllib.request import urlopen, HTTPError
import json as json_lib
import tinys3


__author__ = 'Tim Langeman'
__email__ = "timlangeman@gmail.com"
__copyright__ = "Copyright (C) 2015-2016 Tim Langeman"
__license__ = "MIT"
__version__ = "0.2"


class Quote(models.Model):
    DOC_TYPE_CHOICES = (
        ('html', 'text/html'),
        ('htmls', 'text/html'),
        ('pdf', 'application/pdf'),
        ('text', 'application/plain'),
        ('text', 'text/plain')
    )
    sha1 = models.CharField(
        unique=True,
        max_length=40
        # help_text='Sha1 hash of: citing_quote|citing_url|cited_cited'
    )
    citing_url = models.URLField(
        max_length=2000,
        null=False, blank=False,
        help_text='URL of the text that is citing the quoted text'
    )
    citing_quote = models.TextField(
        null=False, blank=False,
        help_text='quote, as found in citing text'
    )
    citing_quote_length = models.IntegerField(
        null=False, blank=False,
        help_text='The number of characters found in the citing quote'
    )
    citing_quote_start_position = models.IntegerField(
        null=False, blank=False,
        help_text='The starting location of the citing quote \
            (in number of characters)'
    )
    citing_quote_end_position = models.IntegerField(
        null=False, blank=False,
        help_text='The ending location of the citing quote \
            (in number of characters)'
    )
    citing_context_start_position = models.IntegerField(
        null=False, blank=False,
        help_text='The starting location of the citing context \
            (in number of characters)'
    )
    citing_context_end_position = models.IntegerField(
        null=False, blank=False,
        help_text='The ending location of the citing context \
            (in number of characters)'
    )
    citing_context_before = models.TextField(
        null=False, blank=False,
        help_text='The context that preceeds the quote in the citing document'
    )
    citing_context_after = models.TextField(
        null=False, blank=False,
        help_text='The context that follows the quote in the citing document'
    )
    citing_text = models.TextField(
        null=False, blank=False,
        help_text='The text of the citing document'
    )
    citing_doc_type = models.CharField(
        max_length=4,
        choices=DOC_TYPE_CHOICES,
        default="html"
    )
    citing_raw = models.TextField(
        null=False, blank=False,
        help_text='The text/html/pdf source, as originally downloaded'
    )
    citing_archive_url = models.URLField(
        null=True, blank=True,
        help_text='URL of the citing archived copy (ideally at archive.org)'
    )
    citing_cache_url = models.URLField(
        null=True, blank=True,
        help_text="URL of the saved citing copy \
            (private unless the original disappears)"
    )
    citing_download_date = models.DateTimeField(
        null=False, blank=False,
        auto_now_add=True,
        help_text='Date citing document was downloaded'
    )
    cited_url = models.URLField(
        max_length=2000,
        null=False, blank=False,
        help_text='URL of the text that is cited'
    )
    cited_quote = models.TextField(
        null=False, blank=False,
        help_text='quote, as found in cited text'
    )
    cited_quote_length = models.IntegerField(
        null=False, blank=False,
        help_text='The number of characters found in the cited quote'
    )
    cited_quote_start_position = models.IntegerField(
        null=False, blank=False,
        help_text='The starting location of the cited quote \
            (in number of characters)'
    )
    cited_quote_end_position = models.IntegerField(
        null=False, blank=False,
        help_text='The ending location of the cited quote \
            (in number of characters)'
    )
    cited_context_start_position = models.IntegerField(
        null=False, blank=False,
        help_text='The starting location of the cited context \
            (in number of characters)'
    )
    cited_context_end_position = models.IntegerField(
        null=False, blank=False,
        help_text='The ending location of the cited context \
            (in number of characters)'
    )
    cited_context_before = models.TextField(
        null=False, blank=False,
        help_text='The context that preceeds the quote in the cited document'
    )
    cited_context_after = models.TextField(
        null=False, blank=False,
        help_text='The context that follows the quote in the cited document'
    )
    cited_text = models.TextField(
        null=False, blank=False,
        help_text='The text of the cited document'
    )
    cited_doc_type = models.CharField(
        max_length=4,
        choices=DOC_TYPE_CHOICES,
        default="html"
    )
    cited_raw = models.TextField(
        null=False, blank=False,
        help_text='The text/html/pdf source, as originally downloaded'
    )
    cited_archive_url = models.URLField(
        null=True, blank=True,
        help_text='URL of the cited archived copy (ideally at archive.org)'
    )
    cited_cache_url = models.URLField(
        null=True, blank=True,
        help_text="URL of the saved cited copy \
            (private unless the original disappears)"
    )
    cited_download_date = models.DateTimeField(
        null=False, blank=False,
        auto_now_add=True,
        help_text='Date cited document was downloaded'
    )
    create_date = models.DateTimeField(
        null=False, blank=False,
        auto_now_add=True,
        help_text='Date quote record created'
    )
    create_elapsed_time = models.DecimalField(
        null=True, blank=True,
        max_digits=9,
        decimal_places=5,
        help_text='Elapsed time taken to compute neotext record, \
            excluding time to save to db'
    )

    app_label = "neotext"

    def __str__(self):
        return self.citing_quote

    def filename(self):
        """ Name of file stored locally and uploaded to the cloud """
        return ''.join([self.sha1, '.json'])

    def json_url(self):
        return ''.join([
            settings.SITE_READ_URL,
            '/quote/',
            settings.HASH_ALGORITHM, '/',
            settings.VERSION_NUM, '/',
            self.filename()[:2], '/',
            self.filename()
        ])

    def local_filename(self):
        return ''.join([settings.JSON_FILE_PATH, self.filename()])

    def publish_json(self):
        print("Publishing json ..")
        self.save_json_locally()
        filename = self.save_json_to_cloud()
        return filename

    def is_published(self):

        # Get JSON file from remote URL
        public_json_url = self.json_url()
        try:
            public_json_binary = urlopen(public_json_url).read()
        except HTTPError:
            return False
        public_json = public_json_binary.decode('ascii')

        # Test: Is this valid json?
        try:
            json_lib.loads(public_json)
        except ValueError:
            return False
        return True

    def json_fields(self):
        return [
            'sha1',
            'cited_url', 'citing_url',
            'cited_context_before', 'cited_context_after',
            'citing_context_before', 'citing_context_after',
            'citing_quote', 'cited_quote'
        ]

    def json(self, all_fields=False):
        """ json-encoded version of dictionary """
        json_fields = {}
        all_data = self.__dict__
        for field in self.json_fields():
            json_fields[field] = all_data[field]
        return json_lib.dumps(json_fields)

    def save_json_locally(self):
        with open(self.local_filename(), 'w') as f:
            f.write(self.json())
        print("Json saved locally ..")

    def save_json_to_cloud(self):
        """
            Upload json file to Amazon S3
        """
        print('Starting upload json to cloud: ' + self.local_filename())

        f = open(self.local_filename(), 'rb')

        # Divide into subdirectories like git:
        # http://www.quora.com/File-Systems-Why-does-git-shard-the-objects-folder-into-256-subfolders
        shard_folder = self.filename()[:2]
        path_list = (''.join([
            settings.AMAZON_S3_BUCKET,
            "/quote/", settings.HASH_ALGORITHM, '/',
            settings.VERSION_NUM, "/",
            shard_folder
        ]))
        bucket_folder = ''.join(path_list)

        conn = tinys3.Connection(
            settings.AMAZON_ACCESS_KEY,
            settings.AMAZON_SECRET_KEY,
            tls=True,
            endpoint=settings.AMAZON_S3_ENDPOINT
        )
        conn.upload(
            self.filename(), f,
            bucket=bucket_folder,
            content_type='application/json',
            expires='max'
        )
        print("json upload succeeded: " + self.filename())
        return self.filename()
