from django.conf.urls import url
from .views import document_download
from .views import roadmap
from .views import document_intro
from .views import document_tools
from .views import document_collect

urlpatterns = [
	url(r'^$', roadmap, name='roadmap_2'),
	url(r'^roadmap/$', roadmap, name='roadmap'),
	url(r'^intro/$', document_intro, name='document_intro'),
	url(r'^tools/$', document_tools, name='document_tools'),
	url(r'^collect/$', document_collect, name='document_collect'),
	url(r'^download/$', document_download, name='document_download'),
]
