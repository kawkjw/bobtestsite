from django import template

register = template.Library()

@register.filter(name='array_num')
def array_num(value, arg):
	array = []
	array = value
	index = arg
	return array[index]
