import re
from authentication.forms import EditProfileForm, RegisterForm,UploadProfileImageForm
from django.http.response import JsonResponse
from rest_framework.views import APIView
from .repo import *
from core.constants import SUCCEED,FAILED

class ProfileApi(APIView):
    

    def edit_profile(self,request,*args, **kwargs):
        context={'result':FAILED}
        profile_id=0
        if 'profile_id' in kwargs:
            profile_id=kwargs['profile_id']
        log=1
        if request.method=='POST':
            log+=1
            edit_profile_form=EditProfileForm(request.POST)
            if edit_profile_form.is_valid():
                log+=1                
                # profile_id=edit_profile_form.cleaned_data['profile_id']
                first_name=edit_profile_form.cleaned_data['first_name']
                last_name=edit_profile_form.cleaned_data['last_name']
                email=edit_profile_form.cleaned_data['email']
                bio=edit_profile_form.cleaned_data['bio']
                mobile=edit_profile_form.cleaned_data['mobile']
                address=edit_profile_form.cleaned_data['address']
                result=ProfileRepo(request=request).edit_profile(profile_id=profile_id,
                first_name=first_name,
                last_name=last_name,
                email=email,
                bio=bio,
                mobile=mobile,
                address=address,
                )
                if result:
                    context['result']=SUCCEED

        context['log']=log
        return JsonResponse(context)    


    def register_profile(self,request,*args, **kwargs):
        context={'result':FAILED}
        log=1
        if request.method=='POST':
            log=2
            register_form=RegisterForm(request.POST)
            if register_form.is_valid():
                log=3
                first_name=register_form.cleaned_data['first_name']
                last_name=register_form.cleaned_data['last_name']
                bio=register_form.cleaned_data['bio']
                mobile=register_form.cleaned_data['mobile']
                email=register_form.cleaned_data['email']
                address=register_form.cleaned_data['address']
                (profile,result,message)=ProfileRepo(request=request).register(
                    first_name=first_name,
                    last_name=last_name,
                    bio=bio,
                    mobile=mobile,
                    address=address,
                    email=email,
                )
                context['result']=result
                context['message']=message
                
        context['log']=log
        return JsonResponse(context)