from django import template
from ..models import Problem

register = template.Library()

class Counter:
	def __init__(self):
		self.count = 0

	def increment(self):
		self.count += 1

	def setzero(self):
		self.count = 0

@register.inclusion_tag('_all_problems.html', takes_context=True)
def all_problems(context):
	problems = Problem.objects.all()
	request = context['request']
	tcounter = Counter()
	return {'problems': problems, 'counter': tcounter, 'test': request}
