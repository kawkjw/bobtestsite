from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Question(models.Model):
	num = models.AutoField(primary_key=True)
	author = models.ForeignKey('auth.User')
	title = models.CharField(max_length=50, null=True)
	created_date = models.DateField(auto_now_add=True, null=True)
	content = models.TextField(null=True, blank=True)
	comment_num = models.IntegerField(null=True)

	def __unicode__(self):
		return self.title

class Comment(models.Model):
	num = models.AutoField(primary_key=True)
	question = models.ForeignKey(Question)
	author = models.ForeignKey('auth.User')
	created_date = models.DateField(auto_now_add=True, null=True)
	message = models.TextField(null=True, blank=True)
