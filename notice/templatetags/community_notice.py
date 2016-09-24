from django import template
from ..models import Notice

register = template.Library()

rowsPerPage = 2

@register.inclusion_tag('_notice_list.html')
def community_notice():
	noticeList = Notice.objects.order_by('-num')[:5]
	current_page = 1

	totalCnt = Notice.objects.all().count()

	pagingHelperlns = pagingHelper()
	totalPageList = pagingHelperlns.getTotalPageList(totalCnt, rowsPerPage)
	print 'totalPageList', totalPageList

	return {'noticeList': noticeList, 'current_page': current_page, 'totalCnt': totalCnt, 'totalPageList': totalPageList}

class pagingHelper:
	def getTotalPageList(self, total_cnt, rowsPerPage):
		if((total_cnt % rowsPerPage) == 0):
			self.total_pages = total_cnt / rowsPerPage
			print 'getTotalPage #1'
		else:
			self.total_pages = (total_cnt / rowsPerPage) + 1
			print 'getTotalPage #2'

		self.totalPageList = []
		for j in range(self.total_pages):
			self.totalPageList.append(j+1)

		return self.totalPageList

	def __init__(self):
		self.total_pages = 0
		self.totalPageList = 0
