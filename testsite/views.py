from django.shortcuts import render

from django.views.generic.base import TemplateView

from django.views.generic.edit import CreateView
from user_profile.forms import UserCreationForm
from django.core.urlresolvers import reverse_lazy

from user_profile.models import UserProfile
from django.contrib.auth.models import User

from django.http import HttpResponse

class HomeView(TemplateView):
	template_name = 'home.html'

class UserCreateView(CreateView):
	template_name = 'registration/register.html'
	form_class = UserCreationForm
	success_url = reverse_lazy('register_done')

class UserCreateDoneTV(TemplateView):
	template_name = 'registration/register_done.html'

def home(request):
	testuser = User.objects.all()
	level = UserProfile.objects.filter(user_id=testuser)
	return render(request, 'problem/_recommend_problem.html', {'testuser': testuser})

