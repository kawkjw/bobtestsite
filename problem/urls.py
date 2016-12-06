from django.conf.urls import url
from problem.views import artifact1
from problem.views import artifact2
from problem.views import artifact3
from problem.views import artifact4
from problem.views import artifact5
from problem.views import artifact6
from problem.views import artifact7
from problem.views import artifact8
from problem.views import artifact9
from problem.views import artifact10
from problem.views import artifact11
from problem.views import artifact12
from problem.views import artifact13
from problem.views import anti1, anti2, anti3, case1, case2, case3, case4
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
	url(r'^forensic/7/', artifact7, name='artifact7'),
	url(r'^forensic/8/', artifact8, name='artifact8'),
	url(r'^forensic/9/', artifact9, name='artifact9'),
	url(r'^forensic/10/', artifact10, name='artifact10'),
	url(r'^forensic/11/', artifact11, name='artifact11'),
	url(r'^forensic/12/', artifact12, name='artifact12'),
	url(r'^forensic/13/', artifact13, name='artifact13'),
	url(r'^antiforensic/1/', anti1, name='anti1'),
	url(r'^antiforensic/2/', anti2, name='anti2'),
	url(r'^antiforensic/3/', anti3, name='anti3'),
	url(r'^scenario/1/', case1, name='case1'),
	url(r'^scenario/2/', case2, name='case2'),
	url(r'^scenario/3/', case3, name='case3'),
	url(r'^scenario/4/', case4, name='case4'),
	url(r'^view/$', problem_view, name='problem_view'),
	url(r'^write/$', problem_write, name='problem_write'),
	url(r'^write_done/$', problem_write_done, name='problem_write_done'),
	url(r'^answer_check/$', problem_answercheck, name='problem_answercheck'),
	url(r'^download/$', problem_download, name='problem_download'),
]
