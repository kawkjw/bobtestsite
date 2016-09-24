from django.contrib import admin

# Register your models here.

from problem.models import Problem

class ProblemAdmin(admin.ModelAdmin):
	list_display = ('title', 'created_date', 'level', 'artifact')

admin.site.register(Problem, ProblemAdmin)
