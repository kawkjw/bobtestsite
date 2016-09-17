from django.shortcuts import render

# Create your views here.

from django.views.generic import ListView, DetailView
from notice.models import Notice

class NoticeLV(ListView):
	model = Notice
	template_name = 'homepage.html'
