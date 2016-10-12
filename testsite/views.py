import re
from datetime import datetime
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
from django.contrib.auth.models import User
from user_profile.models import UserProfile

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

def register_page(request):
	context = Context({})
	return render(request, 'registration/register.html', context)

def get_user(input_user):
	try:
		return User.objects.get(username=input_user)
	except User.DoesNotExist:
		return None

def register_done(request):
	if request.method == "GET":
		return render(request, 'registration/register.html')
	if request.method == "POST":
		username = request.POST['username']

		m = re.match(r"\d+", username)
		if m != None:
			context = Context({'name_state': True})
			return render(request, 'registration/register.html', context)

		email = request.POST['email']

		m = re.match(r"(\w+[\w\.]*)@(\w+[\w\.]*)\.([A-Za-z]+)", email)
		if m == None:
			context = Context({'email_state': True})
			return render(request, 'registration/register.html', context)

		password1 = request.POST['password1']

		if len(password1) < 8:
			context = Context({'passwordlen_state': True})
			return render(request, 'registration/register.html', context)

		m = re.match(r"\d+", password1)
		if m != None:
			context = Context({'passwordnum_state': True})
			return render(request, 'registration/register.html', context)

		for i in range(0, len(username) - 4):
			if password1.find(username[i:i+5]) != -1:
				context = Context({'password_state': True})
				return render(request, 'registration/register.html', context)

		password2 = request.POST['password2']
		user = get_user(username)
		if password1 == password2:
			if user is None:
				user = User.objects.create_user(username, email, password1)
				user.save()

				user = get_user(username)
				UserProfile.objects.filter(user_id=user.id).update(level = 0)
				UserProfile.objects.filter(user_id=user.id).update(last_submit = datetime.now())
				UserProfile.objects.filter(user_id=user.id).update(score = 0)
				return render(request, 'registration/register_done.html')
			else:
				context = Context({'user_state': True})
				return render(request, 'registration/register.html', context)
		else:
			context = Context({'password_state': True})
			return render(request, 'registration/register.html', context)

class HomeView(TemplateView):
	template_name = 'home.html'

class UserCreateView(CreateView):
	template_name = 'registration/register.html'
	form_class = UserCreationForm
	success_url = reverse_lazy('register_done')

class UserCreateDoneTV(TemplateView):
	template_name = 'registration/register_done.html'

