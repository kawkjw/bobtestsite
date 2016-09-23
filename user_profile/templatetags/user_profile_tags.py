from django import template
from ..models import UserProfile

register = template.Library()

@register.inclusion_tag('_user_history.html')
def user_history():
	profiles = UserProfile.objects.all()
	return {'profiles': profiles}
