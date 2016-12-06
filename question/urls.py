from django.conf.urls import url
from .views import question_list
from .views import question_view
from .views import question_write
from .views import question_write_done
from .views import comment_write_done

urlpatterns = [
	url(r'list/$', question_list, name='question_list'),
	url(r'view/$', question_view, name='question_view'),
	url(r'write/$', question_write, name='question_write'),
	url(r'write/done/$', question_write_done, name='question_write_done'),
	url(r'comment/done/$', comment_write_done, name='comment_write_done'),
]
