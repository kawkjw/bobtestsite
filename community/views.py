from django.shortcuts import render

# Create your views here.

from django.template import Context
from .models import Notice

from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.http import HttpResponseRedirect

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from types import *

def Noticelist(request):
	#notice_list = Notice.objects.order_by('-num')
	page_data = Paginator(Notice.objects.order_by('-num'), 3)
	page = request.GET['page']

	if page is None:
		page = 1
	if type(page) == StringType:
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
