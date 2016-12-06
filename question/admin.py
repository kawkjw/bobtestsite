from django.contrib import admin

# Register your models here.

from .models import Question, Comment

class QuestionAdmin(admin.ModelAdmin):
	list_display = ('num', 'title', 'author', 'created_date')

class CommentAdmin(admin.ModelAdmin):
	list_display = ('num', 'question', 'author', 'created_date')

admin.site.register(Question, QuestionAdmin)
admin.site.register(Comment, CommentAdmin)
