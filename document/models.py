from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Document(models.Model):
	num = models.AutoField(primary_key=True)
	author = models.ForeignKey('auth.User')
	title = models.CharField(max_length=50, null=True)
	created_date = models.DateField(blank=True)
	hits = models.IntegerField(blank=True)
	filelist = models.CharField(max_length=500, null=True, blank=True)

	def __unicode__(self):
		return self.title
