from __future__ import unicode_literals

from django.db import models

# Create your models here.

from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.models import User

class UserProfile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True)
	level = models.PositiveSmallIntegerField(null=True)
	last_submit = models.DateTimeField(null=True, blank=True)
	score = models.IntegerField(null=True, blank=True)
	right_problems = models.CharField(max_length=200, blank=True)

def assure_user_profile_exists(pk):
	user = User.objects.get(pk=pk)
	try:
		# fails if it doesn't exist
		userprofile = user.userprofile
	except UserProfile.DoesNotExist, e:
		userprofile = UserProfile(user=user)
		userprofile.save()
	return

def create_profile(sender, **kwargs):
	user = kwargs["instance"]
	if kwargs["created"]:
		user_profile = UserProfile(user=user)
		user_profile.save()

post_save.connect(create_profile, sender=User)
