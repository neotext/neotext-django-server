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

from django.db import models
from django.core.validators import RegexValidator

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
        max_length=40,
        help_text='Sha1 hash of: citing_quote|citing_url|cited_cited'
		"""
		validators=[RegexValidator(regex='^[A-Fa-f0-9]{4}$', 
			message='Length has to be 40 (hex-digits)', code='nomatch')]
		"""
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
		help_text='The starting location of the citing quote (in number of characters)'
  )
  citing_quote_end_position = models.IntegerField(
		null=False, blank=False,
		help_text='The ending location of the citing quote (in number of characters)'
  )
  citing_context_start_position = models.IntegerField(
		null=False, blank=False,
		help_text='The starting location of the citing context (in number of characters)'
  )
  citing_context_end_position = models.IntegerField(
		null=False, blank=False,
		help_text='The ending location of the citing context (in number of characters)'
  )
  citing_context_before = models.TextField(
		null=False, blank=False,
		help_text='The context that preceeds the quote in the citing document'
  )
  citing_context_after = models.TextField(
		null=False, blank=False,
		help_text='The context that follows the quote in the citing document'
  )
  citing_text= models.TextField(
		null=False, blank=False,
		help_text='The text of the citing document'
  )
  citing_doc_type = models.CharField(max_length=4,
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
		help_text="URL of the saved citing copy (private unless the original disappears)"
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
		help_text='The starting location of the cited quote (in number of characters)'
  )
  cited_quote_end_position = models.IntegerField(
		null=False, blank=False,
		help_text='The ending location of the cited quote (in number of characters)'
  )
  cited_context_start_position = models.IntegerField(
		null=False, blank=False,
		help_text='The starting location of the cited context (in number of characters)'
  )
  cited_context_end_position = models.IntegerField(
		null=False, blank=False,
		help_text='The ending location of the cited context (in number of characters)'
  )
  cited_context_before = models.TextField(
		null=False, blank=False,
		help_text='The context that preceeds the quote in the cited document'
  )
  cited_context_after = models.TextField(
		null=False, blank=False,
		help_text='The context that follows the quote in the cited document'
  )
  cited_text= models.TextField(
		null=False, blank=False,
		help_text='The text of the cited document'
  )
  cited_doc_type = models.CharField(max_length=4,
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
		help_text="URL of the saved cited copy (private unless the original disappears)"
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
		max_digits = 9,
		decimal_places = 5,
		help_text='Elapsed time taken to compute neotext record, excluding time to save to db'
  )

  app_label = "neotext"

  def __str__(self):
        return self.citing_quote

