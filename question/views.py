from django.shortcuts import render

# Create your views here.

from .models import Question, Comment
from django.template import Context

from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.http import HttpResponseRedirect

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def question_list(request):
	page_data = Paginator(Question.objects.order_by('-num'), 5)
	page = request.GET.get('page', 1)

	try:
		question_list = page_data.page(page)
	except PageNotAnInteger:
		question_list = page_data.page(1)
	except EmptyPage:
		question_list = page_data.page(page_data.num_pages)

	last_page = page_data.num_pages
	context = Context({'request': request, 'question_list': question_list, 'current_page': int(page), 'total_page': range(1, page_data.num_pages + 1), 'last_page': last_page})
	return render(request, 'question_list.html', context)

def question_view(request):
	if not request.user.is_active:
		return HttpResponseRedirect('/login_check/')
	question_num = request.GET['qnum']
	question = Question.objects.get(num=question_num)
	comments = Comment.objects.filter(question_id=question_num)
	state = False
	if question.author_id == request.user.id:
		state = True
	if request.user.is_staff:
		state = True

	context = Context({'request': request, 'question': question, 'comments': comments, 'state': state})
	return render(request, 'question_view.html', context)

@login_required(login_url='/login/')
def question_write(request):
	if not request.user.is_active:
		return HttpResponseRedirect('/login_check/')
	return render(request, 'question_write.html')

@login_required(login_url='/login/')
def question_write_done(request):
	if not request.user.is_active:
		return HttpResponseRedirect('/login_check/')
	if request.method == "GET":
		return render(request, 'question_write.html')
	if request.method == "POST":
		question = Question(title = request.POST['title'], author_id = request.user.id, content = request.POST['content'], comment_num = 0)
		question.save()
	return render(request, 'question_write_done.html')

def comment_write_done(request):
	try:
		question_num = request.GET['qnum']
		question = Question.objects.get(num=question_num)
		comment_m = request.POST['message']
	except:
		return HttpResponseRedirect('/question/list/')

	if comment_m is None:
		return HttpResponseRedirect('/')

	comment = Comment(question_id = question_num, author_id = request.user.id, message = comment_m)
	comment.save()

	Question.objects.filter(num=question_num).update(comment_num = question.comment_num + 1)

	return HttpResponseRedirect('/question/view/?qnum=' + question_num)
