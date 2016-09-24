from django.shortcuts import render

from django.views.generic.base import TemplateView

from django.views.generic.edit import CreateView
from user_profile.forms import UserCreationForm
from django.core.urlresolvers import reverse_lazy

from django.http.response import HttpResponse

from django.template import Context
from django.template.loader import get_template

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

