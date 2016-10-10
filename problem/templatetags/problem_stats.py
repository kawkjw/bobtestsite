from django import template

register = template.Library()

@register.filter(name='getstats')
def getstats(value, arg):
	corrects = value
	submits = arg

	if submits == 0:
		return "0%"
	else:
		stats = float(corrects) / submits
		stats = round(stats * 100, 2)
		stats_str = str(stats) + '%'
		return stats_str
