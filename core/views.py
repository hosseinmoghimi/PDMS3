from django.shortcuts import render
from .settings import *
from authentication.repo import ProfileRepo
# Create your views here.
def CoreContext(request,*args, **kwargs):
    context = {}
    app_name = 'core'
    context['wide_layout_parent']="phoenix/wide-layout.html"
    context['help_title']="راهنما"
    if 'app_name' in kwargs:
        app_name = kwargs['app_name']
    context['user'] = request.user
    context['profile'] = ProfileRepo(request=request).me
    context['APP_NAME'] = app_name
     
    context[app_name+'_sidebar'] = True
    context['DEBUG'] = DEBUG
    context['ADMIN_URL'] = ADMIN_URL
    context['MEDIA_URL'] = MEDIA_URL
    context['SITE_URL'] = SITE_URL

    return context