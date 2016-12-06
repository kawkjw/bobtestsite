from django.contrib import admin

# Register your models here.

from .models import Notice
from .models import Freeboard, Comment_c

class NoticeAdmin(admin.ModelAdmin):
	list_display = ('num', 'title', 'created_date')

class FreeboardAdmin(admin.ModelAdmin):
	list_display = ('num', 'title', 'author', 'created_date')

class CommentAdmin(admin.ModelAdmin):
	list_display = ('num', 'freeboard', 'author', 'created_date')

admin.site.register(Notice, NoticeAdmin)
admin.site.register(Freeboard, FreeboardAdmin)
admin.site.register(Comment_c, CommentAdmin)
