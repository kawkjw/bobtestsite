import re
from datetime import datetime
from django.shortcuts import render

from django.views.generic.base import TemplateView

from django.views.generic.edit import CreateView
from user_profile.forms import UserCreationForm
from django.core.urlresolvers import reverse_lazy

from django.http import HttpResponse, HttpResponseRedirect

from django.template import Context
from django.template.loader import get_template

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from user_profile.models import UserProfile

def beenLimited(request, exception):
	problem_num = request.GET['pnum']
	context = Context({'problem_num': problem_num})
	return render(request, 'brute_forcing.html', context)

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

def set_rank():
	users = UserProfile.objects.order_by('-score')
	current_rank = 1
	counter = 0
	same = 1

	for user in users:
		if counter < 1:
			UserProfile.objects.filter(user_id=user.user_id).update(rank = current_rank)
		else:
			if user.score == users[counter - 1].score:
				UserProfile.objects.filter(user_id=user.user_id).update(rank = current_rank)
				same += 1
			else:
				current_rank += same
				if same != 1:
					same = 1
				UserProfile.objects.filter(user_id=user.user_id).update(rank = current_rank)
		counter += 1

@login_required(login_url='/login/')
def mypage(request):
	if not request.user.is_active:
		return HttpResponseRedirect('/login/')
	set_rank()
	profile = UserProfile.objects.get(user_id=request.user.id)
	lists = profile.right_problems.split(',')
	right_problems = []
	for i in range(0, len(lists) - 1):
		right_problems.append(lists[i])
	last_problem = len(right_problems)
	context = Context({'profile': profile, 'right_problems': right_problems, 'last_problem': last_problem})
	return render(request, 'mypage.html', context)

@login_required(login_url='/login/')
def rank_page(request):
	set_rank()
	names = User.objects.filter(is_staff=False)
	users = UserProfile.objects.order_by('rank')[0:10]
	context = Context({'users': users, 'names': names})

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

