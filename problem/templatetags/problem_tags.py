from django import template
from ..models import Problem

register = template.Library()

@register.inclusion_tag('_recommend_problem.html')
def recommend_problem():
	problems = Problem.objects.all()
	return {'problems': problems}
