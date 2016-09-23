from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Problem(models.Model):
	num = models.AutoField(primary_key=True)
	title = models.CharField(max_length=50, blank=True)
	author = models.ForeignKey('auth.User')
	created_date = models.DateField(blank=True)
	level = models.PositiveSmallIntegerField(null=True)
	content = models.TextField(null=True, blank=True)

	def __str__(self):
		return self.title
