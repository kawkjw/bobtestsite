import os
import urllib
from django.shortcuts import render

# Create your views here.

from django.template import Context
from .models import Document

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, StreamingHttpResponse
from django.utils.encoding import smart_unicode

def roadmap(request):
	return render(request, 'roadmap/roadmap.html')

def document_list(request):
	documents = Document.objects.order_by('num')
	context = Context({'documents': documents})
	return render(request, 'document_list.html', context)

@login_required(login_url='/login/')
def document_view(request):
	if not request.user.is_active:
		return HttpResponseRedirect('/login_check/')
	document_num = request.GET['dnum']
	document = Document.objects.get(num=document_num)
	state = True
	files = document.filelist.split('/')
	if files[0] == '':
		state = False
	context = Context({'document': document, 'state': state, 'filename': files, 'size': range(0, len(files))})
	return render(request, 'documents/' + str(document_num) + '.html', context)

@login_required(login_url='/login/')
def document_download(request):
	if not request.user.is_active:
		return HttpResponseRedirect('/login_check/')
	filename = urllib.unquote(request.GET['filename'])
	DOC_DIR = os.path.dirname(os.path.abspath(__file__))
	fp = open(unicode(os.path.join(DOC_DIR, 'document_file')+'/'+filename), 'r')
	response = StreamingHttpResponse(fp, content_type='application/force-download')
	response['Content-Disposition'] = u'attachment; filename*=UTF-8\'\'%s' % urllib.quote(filename.encode('utf-8'))
	return response
