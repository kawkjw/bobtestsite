from django.shortcuts import render

# Create your views here.

from django.template import Context
from .models import Notice
from .models import Freeboard, Comment_c

from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.http import HttpResponseRedirect

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def community1(request):
	return render(request, 'community_1.html')

def community2(request):
	return render(request, 'community_2.html')

def freeboard_list(request):
	page_data = Paginator(Freeboard.objects.order_by('-num'), 5)
	page = request.GET.get('page', 1)

	try:
		freeboard_list = page_data.page(page)
	except PageNotAnInteger:
		freeboard_list = page_data.page(1)
	except EmptyPage:
		freeboard_list = page_data.page(page_data.num_pages)

	last_page = page_data.num_pages
	context = Context({'request': request, 'freeboard_list': freeboard_list, 'current_page': int(page), 'total_page': range(1, page_data.num_pages + 1), 'last_page': last_page})
	return render(request, 'freeboard/freeboard_list.html', context)

def freeboard_view(request):
	if not request.user.is_active:
		return HttpResponseRedirect('/login_check/')
	freeboard_num = request.GET['fnum']
	freeboard = Freeboard.objects.get(num=freeboard_num)
	comments = Comment_c.objects.filter(freeboard_id=freeboard_num)
	context = Context({'request': request, 'freeboard': freeboard, 'comments': comments})
	return render(request, 'freeboard/freeboard_view.html', context)

@login_required(login_url='/login/')
def freeboard_write(request):
	if not request.user.is_active:
		return HttpResponseRedirect('/login_check/')
	return render(request, 'freeboard/freeboard_write.html')

@login_required(login_url='/login/')
def freeboard_write_done(request):
	if not request.user.is_active:
		return HttpResponseRedirect('/login_check/')
	if request.method == "GET":
		return render(request, 'freeboard_write.html')
	if request.method == "POST":
		freeboard = Freeboard(title = request.POST['title'], author_id = request.user.id, content = request.POST['content'], f_comment_num = 0)
		freeboard.save()
	return render(request, 'freeboard/freeboard_write_done.html')

def comment_write_done(request):
	try:
		freeboard_num = request.GET['fnum']
		freeboard = Freeboard.objects.get(num=freeboard_num)
		comment_m = request.POST['message']
	except:
		return HttpResponseRedirect('/community/freeboard/list/')

	if comment_m is None:
		return HttpResponseRedirect('/')

	comment = Comment_c(freeboard_id = freeboard_num, author_id = request.user.id, message = comment_m)
	comment.save()

	Freeboard.objects.filter(num=freeboard_num).update(f_comment_num = freeboard.f_comment_num + 1)

	return HttpResponseRedirect('/community/freeboard/view/?fnum=' + freeboard_num)

def Noticelist(request):
	page_data = Paginator(Notice.objects.order_by('-num'), 5)
	page = request.GET.get('page', 1)

	if page is None:
		page = 1

	try:
		notice_list = page_data.page(page)
	except PageNotAnInteger:
		notice_list = page_data.page(1)
	except EmptyPage:
		notice_list = page_data.page(page_data.num_pages)

	last_page = page_data.num_pages
	context = Context({'request': request, 'notice_list': notice_list, 'current_page': int(page), 'total_page': range(1, page_data.num_pages + 1), 'last_page': last_page})
	return render(request, 'notice/notice_list.html', context)

@login_required(login_url='/login/')
def Noticeview(request):
	if not request.user.is_active:
		return HttpResponseRedirect('/login_check/')
	notice_num = request.GET['nnum']
	notice = Notice.objects.get(num=notice_num)
	Notice.objects.filter(num=notice_num).update(hits = notice.hits + 1)
	context = Context({'request': request, 'notice': notice})
	return render(request, 'notice/notice_view.html', context)

@login_required(login_url='/login/')
def Noticewrite(request):
	context = Context({})
	if not request.user.is_staff:
		return HttpResponseRedirect('/')
	return render(request, 'notice/notice_write.html', context)

def Noticewritedone(request):
	context = Context({})
	if not request.user.is_staff:
		return HttpResponseRedirect('/')
	if request.method == "GET":
		return render(request, 'notice/notice_write.html', context)
	if request.method == "POST":
		notice = Notice(title = request.POST['title'], created_date = datetime.now(), author_id = request.user.id, content = request.POST['content'], hits = 0)
		notice.save()
	return render(request, 'notice/notice_write_done.html', context)
