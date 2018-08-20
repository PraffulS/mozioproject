# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class providers(models.Model):
    providerName = models.CharField(max_length=200, null=False)
    providerEmail = models.CharField(max_length=100, null=False)
    providerNo = models.CharField(max_length=50, null=False)
    providerLanguage = models.CharField(max_length=50, null=False)
    providerCurrency = models.CharField(max_length=50, null=False)
    class Meta:
        db_table = 'providers'

class serviceAreas(models.Model):
	name = models.CharField(max_length=200, null=False)
	price = models.CharField(max_length=50, null=False)
	geometry = models.TextField(default="", null=False)
	forProviderId = models.ForeignKey(providers)
	class Meta:
		db_table = 'serviceAreas'