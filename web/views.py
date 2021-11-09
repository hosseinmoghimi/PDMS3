import json
from django.http.response import Http404
from .apps import APP_NAME
from .forms import *
from django.views import View
from django.shortcuts import redirect, render
TEMPLATE_ROOT = APP_NAME+"/"
LAYOUT_PARENT=""

def getContext(request):
    context={}
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    return context

 

class BasicViews(View):
     
    def home(self, request, *args, **kwargs):
        context = getContext(request)
        context['name']='web'
        return render(request, TEMPLATE_ROOT+"index.html", context)

