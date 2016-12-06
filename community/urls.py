from django.conf.urls import url
from .views import Noticelist
from .views import Noticeview
from .views import Noticewrite
from .views import Noticewritedone
from .views import freeboard_list
from .views import freeboard_view
from .views import freeboard_write
from .views import freeboard_write_done
from .views import comment_write_done

urlpatterns = [
	url(r'^freeboard/list/$', freeboard_list, name='freeboard_list'),
	url(r'^freeboard/view/$', freeboard_view, name='freeboard_view'),
	url(r'^freeboard/write/$', freeboard_write, name='freeboard_write'),
	url(r'^freeboard/write/done/$', freeboard_write_done, name='freeboard_write_done'),
	url(r'^freeboard/comment/done/$', comment_write_done, name='f_comment_write_done'),
]
