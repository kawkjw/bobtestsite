from django.contrib import admin

# Register your models here.

from notice.models import Notice

class NoticeAdmin(admin.ModelAdmin):
	list_display = ('title', 'created_date')

admin.site.register(Notice, NoticeAdmin)
