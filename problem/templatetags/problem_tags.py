from django import template
from ..models import Problem
from user_profile.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

register = template.Library()

@register.inclusion_tag('_recommend_problem.html', takes_context=True)
def recommend_problem(context):
	problems = Problem.objects.all()
	tprofiles = UserProfile.objects.all()
	tusers = User.objects.all()
	request = context['request']
	ttusers = request.session
	return {'problems': problems, 'tprofiles': tprofiles, 'tusers': tusers, 'ttusers': ttusers}
