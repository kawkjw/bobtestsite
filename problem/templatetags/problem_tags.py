from django import template
from ..models import Problem
from user_profile.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

register = template.Library()

class Counter:
	def __init__(self):
		self.count = 1
	
	def increment(self):
		self.count += 1

@register.inclusion_tag('_recommend_problem.html', takes_context=True)
def recommend_problem(context):
	problems = Problem.objects.all().order_by('?')[:15]
	tprofiles = UserProfile.objects.all()
	request = context['request']
	tcounter = Counter()
	return {'problems': problems, 'test': request, 'profiles': tprofiles, 'counter': tcounter}
