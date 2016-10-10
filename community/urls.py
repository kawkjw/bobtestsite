from django.conf.urls import url
from community.views import Noticelist
from community.views import Noticeview
from community.views import Noticewrite
from community.views import Noticewritedone

urlpatterns = [
	url(r'^notice/list/$', Noticelist, name='noticelist'),
	url(r'^notice/view/$', Noticeview, name='noticeview'),
	url(r'^notice/write/$', Noticewrite, name='noticewrite'),
	url(r'^notice/write/done/$', Noticewritedone, name='noticewritedone'),
]
