from django.contrib import admin

# Register your models here.

from .models import Document

class DocumentAdmin(admin.ModelAdmin):
	list_display = ('num', 'title', 'created_date')

admin.site.register(Document, DocumentAdmin)
