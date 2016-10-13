from django.contrib import admin

# Register your models here.

from problem.models import Problem
from problem.models import Answerlog

class ProblemAdmin(admin.ModelAdmin):
	list_display = ('num', 'title', 'created_date', 'level', 'artifact')

class AnswerlogAdmin(admin.ModelAdmin):
	list_display = ('num', 'problem_num', 'problem_title', 'submit_answer', 'submitter', 'submit_date')

admin.site.register(Problem, ProblemAdmin)
admin.site.register(Answerlog, AnswerlogAdmin)
