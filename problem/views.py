import os
from django.shortcuts import render

# Create your views here.

from django.contrib.auth.models import User
from user_profile.models import UserProfile

from .models import Problem
from .models import Answerlog
from django.template import Context

from datetime import datetime
from django.http import HttpResponseRedirect, HttpResponse

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
	state = False
	problem_num = request.GET['pnum']
	problem = Problem.objects.get(num=problem_num)
	if problem.tags is not None:
		problem_tags = problem.tags.split('/')
		blank_number = 5 - len(problem_tags) + 1
	else:
		problem_tags = ""
		blank_number = 5
	if request.user.is_active:
		current_user = request.user.id
		user_level = UserProfile.objects.get(user_id=current_user).level
		right_problems = UserProfile.objects.get(user_id=current_user).right_problems.split(',')
		for i in range(0, len(right_problems) - 1):
			if int(right_problems[i]) == problem.num:
				state = True
				break
		context = Context({'problem': problem, 'test': request, 'user_level': user_level, 'state': state, 'problem_tags': problem_tags, 'blank': blank_number})
	else:
		context = Context({'problem': problem, 'test': request, 'problem_tags': problem_tags, 'blank': blank_number})
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
		if 'uploadfile' in request.FILES:
			problem = Problem(title = request.POST['title'], created_date = datetime.now(), content = request.POST['content'], author_id = request.user.id, level = request.POST['level'], artifact = request.POST['artifact'], right_answer = request.POST['right_answer'], corrects = 0, submits = 0, score = request.POST['score'], tags = request.POST['tags'], importance = request.POST['importance'], difficulty = request.POST['difficulty'], downfile = request.FILES['uploadfile'])
			problem.save()
		else:
			return render(request, 'problem_write.html', context)
	return render(request, 'problem_write_done.html', context)

def problem_download(request):
	problem_num = request.GET['pnum']
	problem = Problem.objects.get(num=problem_num)
	fp = open('/home/jinwoo/testsite/media/'+str(problem.downfile), 'r')
	response = HttpResponse(fp, content_type='application/force-download')
	response['Content-Disposition'] = 'attachment; filename="%s"' % str(problem.downfile)
	return response

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
	if problem.right_answer.lower() == answer.lower():
		Problem.objects.filter(num=problem_num).update(corrects = problem.corrects + 1)
		profile = UserProfile.objects.get(user_id=request.user.id)
		UserProfile.objects.filter(user_id=request.user.id).update(right_problems = profile.right_problems + str(problem_num) +',')
		UserProfile.objects.filter(user_id=request.user.id).update(score = profile.score + problem.score)
		state = True
	else:
		state = False

	context = Context({'problem_num': problem_num, 'state': state})
	return render(request, 'problem_answercheck.html', context)

def artifact1(request):
	orderby = request.GET.get('orderby')
	if orderby is None:
		orderby = 'title'

	if str(orderby) == "title":
		problems = Problem.objects.filter(artifact="1").order_by("title")
	elif str(orderby) == "rtitle":
		problems = Problem.objects.filter(artifact="1").order_by("-title")
	elif str(orderby) == "level":
		problems = Problem.objects.filter(artifact="1").order_by("level")
	elif str(orderby) == "rlevel":
		problems = Problem.objects.filter(artifact="1").order_by("-level")
	elif str(orderby) == "stats":
		problems = Problem.objects.raw('select * from problem_problem where artifact=1 order by CAST(corrects AS float) / (case when submits=0 then CAST(1 AS float) else CAST(submits AS float) end)')
	elif str(orderby) == "rstats":
		problems = Problem.objects.raw('select * from problem_problem where artifact=1 order by (CAST(corrects AS float) / (case when submits=0 then CAST(1 AS float) else CAST(submits AS float) end)) DESC')
	else:
		problems = Problem.objects.filter(artifact="1").order_by("title")
	tcounter = Counter()
	context = Context({'problems': problems, 'counter': tcounter, 'request': request})
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
