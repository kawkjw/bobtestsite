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

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from user_profile.models import UserProfile

from django.utils.http import is_safe_url

class Counter:
	def __init__(self):
		self.count = 0
	
	def increment(self):
		self.count += 1

	def setzero(self):
		self.count = 0

def beenLimited(request, exception):
	message = "A few too many tries now. Please try again after 30 seconds."
	return HttpResponse(message)

def login_check(request):
	return render(request, 'login_check.html')

def user_login(request):
	logout(request)
	username = password = ''
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/')
	context = Context({})
	return render(request, 'registration/user_login.html', context)

@login_required(login_url='/login/')
def my_password_change(request):
	if not request.user.is_active:
		return HttpResponseRedirect('/')
	return render(request, 'registration/password_change_form.html')

def my_password_change_done(request):
	if not request.user.is_active:
		return HttpResponseRedirect('/')
	if request.method == "GET":
		return HttpResponseRedirect('/')
	if request.method == "POST":
		old_password = request.POST['old_password']

		if not request.user.check_password(old_password):
			context = Context({'not_old_password': True})
			return render(request, 'registration/password_change_form.html', context)

		new_password1 = request.POST['new_password1']
		new_password2 = request.POST['new_password2']

		if len(new_password1) < 8:
			context = Context({'passwordlen_state': True})
			return render(request, 'registration/password_change_form.html', context)

		m = re.match(r"\d+", new_password1)
		if m != None:
			context = Context({'passwordnum_state': True})
			return render(request, 'registration/password_change_form.html', context)

		for i in range(0, len(request.user.username) - 4):
			if new_password1.find(request.user.username[i:i+5]) != -1:
				context = Context({'password_state': True})
				return render(request, 'registration/password_change_form.html', context)

		if old_password == new_password1:
			context = Context({'same_old_password': True})
			return render(request, 'registration/password_change_form.html', context)

		if request.user.check_password(old_password):
			if new_password1 and new_password2:
				if new_password1 == new_password2:
					request.user.set_password(new_password1)
					request.user.save()
					update_session_auth_hash(request, request.user)
					return render(request, 'registration/password_change_done.html')
				else:
					context = Context({'different': True})
					return render(request, 'registration/password_change_form.html', context)
		else:
			context = Context({'not_old_password': True})
			return render(request, 'registration/password_change_form.html', context)
	return render(request, 'registration/password_change_form.html')

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

@login_required(login_url='/login/')
def rank_page(request):
	scores = UserProfile.objects.order_by('-score')
	users = User.objects.filter(is_staff=False)
	rank = Counter()
	context = Context({'scores': scores, 'users': users, 'rank': rank})

	return render(request, 'rank_page.html', context)

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
			context = Context({'different_password': True})
			return render(request, 'registration/register.html', context)

class HomeView(TemplateView):
	template_name = 'home.html'

class UserCreateView(CreateView):
	template_name = 'registration/register.html'
	form_class = UserCreationForm
	success_url = reverse_lazy('register_done')

class UserCreateDoneTV(TemplateView):
	template_name = 'registration/register_done.html'

