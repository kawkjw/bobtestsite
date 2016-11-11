from django.conf.urls import url
from .views import document_list
from .views import document_view
from .views import document_download
from .views import roadmap

urlpatterns = [
	url(r'^$', roadmap, name='roadmap_2'),
	url(r'^roadmap/$', roadmap, name='roadmap'),
	url(r'^list/$', document_list, name='document_list'),
	url(r'^view/$', document_view, name='document_view'),
	url(r'^download/$', document_download, name='document_download'),
]
