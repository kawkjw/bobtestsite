from django.shortcuts import render

# Create your views here.

from django.contrib.auth.models import User
from user_profile.models import UserProfile

from .models import Problem
from .models import Answerlog
from django.template import Context

from datetime import datetime
from django.http import HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from ratelimit.decorators import ratelimit

class Counter:
	def __init__(self):
		self.count = 0
	
	def increment(self):
		self.count += 1
	
	def setzero(self):
		self.count = 0

def all_problem_test(request):
	problems = Problem.objects.all()
	tcounter = Counter()
	context = Context({'problems': problems, 'counter': tcounter, 'test': request})
	return render(request, '_all_problems.html', context)
@login_required(login_url='/login/')
def problem_view(request):
	problem_num = request.GET['pnum']
	problem = Problem.objects.get(num=problem_num)
	if request.user.is_active:
		current_user = request.user.id
		user_level = UserProfile.objects.get(user_id=current_user).level
		context = Context({'problem': problem, 'test': request, 'user_level': user_level})
	else:
		context = Context({'problem': problem, 'test': request})
	return render(request, 'problem_view.html', context)

@login_required(login_url='/login/')
def problem_write(request):
	context = Context({})
	if not request.user.is_staff:
		return HttpResponseRedirect('/')
	return render(request, 'problem_write.html', context)

def problem_write_done(request):
	context = Context({})
	if not request.user.is_staff:
		return HttpResponseRedirect('/')
	if request.method == "GET":
		return render(request, 'problem_write.html', context)
	if request.method == "POST":
		problem = Problem(title = request.POST['title'], created_date = datetime.now(), content = request.POST['content'], author_id = request.user.id, level = request.POST['level'], artifact = request.POST['artifact'], right_answer = request.POST['right_answer'], corrects = 0, submits = 0)
		problem.save()
	return render(request, 'problem_write_done.html', context)

@ratelimit(key='ip', rate='2/m', block=True)
def problem_answercheck(request):
	try:
		problem_num = request.GET['pnum']
		problem = Problem.objects.get(num=problem_num)
		answer = request.POST['answer']
	except:
		return HttpResponseRedirect('/')

	if answer is None:
		return HttpResponseRedirect('/')

	answerlog = Answerlog(submitter_id = request.user.id, submit_answer = answer)
	answerlog.save()

	Problem.objects.filter(num=problem_num).update(submits = problem.submits + 1)
	if problem.right_answer == answer:
		Problem.objects.filter(num=problem_num).update(corrects = problem.corrects + 1)
		state = True
	else:
		state = False

	context = Context({'problem_num': problem_num, 'state': state})
	return render(request, 'problem_answercheck.html', context)

def artifact1(request):
	problems_bytitle = Problem.objects.filter(artifact="1").order_by("title")
	problems_bylevel = Problem.objects.filter(artifact="1").order_by("level")
	problems_bystats = Problem.objects.raw('select * from problem_problem where artifact=1 order by CAST(corrects AS float) / (case when submits=0 then CAST(1 AS float) else CAST(submits AS float) end)')
	tcounter = Counter()
	context = Context({'problems_bytitle': problems_bytitle, 'problems_bylevel': problems_bylevel, 'problems_bystats': problems_bystats, 'counter': tcounter, 'request': request})
	return render(request, 'artifact1/list.html', context)

def artifact2(request):
	problems_bytitle = Problem.objects.filter(artifact="2").order_by("title")
	problems_bylevel = Problem.objects.filter(artifact="2").order_by("level")
	problems_bystats = Problem.objects.raw('select * from problem_problem where artifact=1 order by CAST(corrects AS float) / (case when submits=0 then CAST(1 AS float) else CAST(submits AS float) end)')
	tcounter = Counter()
	context = Context({'problems_bytitle': problems_bytitle, 'problems_bylevel': problems_bylevel, 'problems_bystats': problems_bystats, 'counter': tcounter, 'request': request})
	return render(request, 'artifact2/list.html', context)

def artifact3(request):
	problems_bytitle = Problem.objects.filter(artifact="3").order_by("title")
	problems_bylevel = Problem.objects.filter(artifact="3").order_by("level")
	problems_bystats = Problem.objects.raw('select * from problem_problem where artifact=1 order by CAST(corrects AS float) / (case when submits=0 then CAST(1 AS float) else CAST(submits AS float) end)')
	tcounter = Counter()
	context = Context({'problems_bytitle': problems_bytitle, 'problems_bylevel': problems_bylevel, 'problems_bystats': problems_bystats, 'counter': tcounter, 'request': request})
	return render(request, 'artifact3/list.html', context)

def artifact4(request):
	problems_bytitle = Problem.objects.filter(artifact="4").order_by("title")
	problems_bylevel = Problem.objects.filter(artifact="4").order_by("level")
	problems_bystats = Problem.objects.raw('select * from problem_problem where artifact=1 order by CAST(corrects AS float) / (case when submits=0 then CAST(1 AS float) else CAST(submits AS float) end)')
	tcounter = Counter()
	context = Context({'problems_bytitle': problems_bytitle, 'problems_bylevel': problems_bylevel, 'problems_bystats': problems_bystats, 'counter': tcounter, 'request': request})
	return render(request, 'artifact4/list.html', context)

def artifact5(request):
	problems_bytitle = Problem.objects.filter(artifact="5").order_by("title")
	problems_bylevel = Problem.objects.filter(artifact="5").order_by("level")
	problems_bystats = Problem.objects.raw('select * from problem_problem where artifact=1 order by CAST(corrects AS float) / (case when submits=0 then CAST(1 AS float) else CAST(submits AS float) end)')
	tcounter = Counter()
	context = Context({'problems_bytitle': problems_bytitle, 'problems_bylevel': problems_bylevel, 'problems_bystats': problems_bystats, 'counter': tcounter, 'request': request})
	return render(request, 'artifact5/list.html', context)
