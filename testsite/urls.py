"""testsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from testsite.views import HomeView
from testsite.views import UserCreateView, UserCreateDoneTV

from testsite.views import user_login, login_check
from testsite.views import intro, documents, problems, community, mypage

urlpatterns = [
    url(r'^admin/', admin.site.urls),

	url(r'^login/$', user_login, name='user_login'),
	url(r'^login_check/$', login_check, name='login_check'),

	url(r'^accounts/', include('django.contrib.auth.urls')),
	url(r'^accounts/register/$', UserCreateView.as_view(), name='register'),
	url(r'^accounts/register/done/$', UserCreateDoneTV.as_view(), name='register_done'),

	url(r'^$', HomeView.as_view(), name='home'),

	url(r'^intro/$', intro, name='intro'),
	url(r'^documents/$', documents, name='documents'),
	# url(r'^problems/$', problems, name='problems'),
	url(r'^problems/', include('problem.urls')),
	# url(r'^community/$', community, name='community'),
	url(r'^community/', include('community.urls')),
	url(r'^mypage/$', mypage, name='mypage'),
]
