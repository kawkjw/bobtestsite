from django.shortcuts import render

# Create your views here.

from django.contrib.auth.models import User
from user_profile.models import UserProfile

def _recommend_problem(request):
	user = User.objects.filter(is_active=True)
	level = UserProfile.objects.filter(user_id=user)
	return render(request, '_recommend_problem.html', {'user': user})
