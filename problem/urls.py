from django.conf.urls import url
from problem.views import artifact1
from problem.views import artifact2
from problem.views import artifact3
from problem.views import artifact4
from problem.views import artifact5
from problem.views import artifact6
from problem.views import problem_view
from problem.views import problem_write
from problem.views import problem_write_done
from problem.views import problem_answercheck
from problem.views import problem_download

urlpatterns = [
	url(r'^forensic/1/', artifact1, name='artifact1'),
	url(r'^forensic/2/', artifact2, name='artifact2'),
	url(r'^forensic/3/', artifact3, name='artifact3'),
	url(r'^forensic/4/', artifact4, name='artifact4'),
	url(r'^forensic/5/', artifact5, name='artifact5'),
	url(r'^forensic/6/', artifact6, name='artifact6'),
	url(r'^view/$', problem_view, name='problem_view'),
	url(r'^write/$', problem_write, name='problem_write'),
	url(r'^write_done/$', problem_write_done, name='problem_write_done'),
	url(r'^answer_check/$', problem_answercheck, name='problem_answercheck'),
	url(r'^download/$', problem_download, name='problem_download'),
]
