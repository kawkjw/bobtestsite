from django.shortcuts import render

from django.views.generic.base import TemplateView

from django.views.generic.edit import CreateView
from user_profile.forms import UserCreationForm
from django.core.urlresolvers import reverse_lazy

from django.http import HttpResponse, HttpResponseRedirect
from django.utils.http import is_safe_url

from django.template import Context
from django.template.loader import get_template

from django.contrib.auth import authenticate, login, logout

def beenLimited(request, exception):
	message = "A few too many tries now. Please try again later."
	return HttpResponse(message)

def login_check(request):
	return render(request, 'login_check.html')

def user_login(request):
	logout(request)
	username = password = ''
	if request.POST:
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/')
	context = Context({})
	return render(request, 'registration/user_login.html', context)

def intro(request):
	template = get_template('intro.html')
	context = Context({'test': request})

	#return HttpResponse(template.render(context))
	return render(request, 'intro.html', context)

def documents(request):
	template = get_template('documents.html')
	context = Context({})

	#return HttpResponse(template.render(context))
	return render(request, 'documents.html', context)

def problems(request):
	template = get_template('problems.html')
	context = Context({})

	#return HttpResponse(template.render(context))
	return render(request, 'problems.html', context)

def community(request):
	template = get_template('community.html')
	context = Context({})

	#return HttpResponse(template.render(context))
	return render(request, 'community.html', context)

def mypage(request):
	context = Context({})

	return render(request, 'mypage.html', context)

class HomeView(TemplateView):
	template_name = 'home.html'

class UserCreateView(CreateView):
	template_name = 'registration/register.html'
	form_class = UserCreationForm
	success_url = reverse_lazy('register_done')

class UserCreateDoneTV(TemplateView):
	template_name = 'registration/register_done.html'

