from django.conf.urls import url
from .views import document_list
from .views import document_view
from .views import document_download

urlpatterns = [
	url(r'^$', document_list, name='document_list'),
	url(r'^view/$', document_view, name='document_view'),
	url(r'^download/$', document_download, name='document_download'),
]
