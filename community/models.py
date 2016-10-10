from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Notice(models.Model):
	num = models.AutoField(primary_key=True)
	author = models.ForeignKey('auth.User')
	title = models.CharField(max_length=50, null=True)
	created_date = models.DateField(blank=True)
	hits = models.IntegerField(blank=True)
	content = models.TextField(null=True, blank=True)

	def __str__(self):
		return self.title
