"""HRManage URL Configuration

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
from django.conf.urls import url
from . import views


urlpatterns = [

    url(r'^RegisterSME$', views.register_sme, name='RegisterSME'),
    url(r'^RegisterHRM$',views.register_hrm,name='RegisterHRM'),
    url(r'^RegisterHRP$',views.register_hrp,name='RegisterHRP'),
    url(r'^application$',views.application,name='ViewApplication'),
    url(r'^CreateCompany$',views.create_company_view,name='CreateCompany'),
    url(r'^CreateCategory$',views.create_category_view,name='CreateCategory'),
    url(r'^PostJob$',views.post_job_view,name='PostJob'),
    url(r'^register$',views.register_view,name='register'),
    url(r'^logout$',views.logout_view,name='logout'),
    url(r'^login$',views.login_view,name='login'),
    url(r'^$',views.index,name='index'),
    url(r'^apply$', views.apply, name='ApplyJob'),
    url(r'^apply/(?P<job>[0-9]+)$',views.apply_job,name='ApplyJob'),
    url(r'^application/(?P<job>[0-9]+)$',views.get_all_apply,name='GetAllApply'),
    url(r'^rate$', views.rate_all_apply, name='RateAllApply'),
    url(r'^rate/(?P<var_apply>[0-9]+)$',views.rate_apply,name='RateApply'),
    url(r'^GetTopFive$',views.get_top_five,name='GetTopFive'),
    url(r'^ApiJson',views.api_json,name='ApiJson'),
]
