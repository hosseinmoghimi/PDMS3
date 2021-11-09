from django.db.models.query import EmptyQuerySet
from core.constants import FAILED, SUCCEED
from django.http.response import Http404
from authentication.serializers import ProfileSerializer
from .settings import SITE_URL
from django.shortcuts import render,redirect
from .repo import *
import json
from .forms import *
from django.views import View
from core.views import CoreContext

TEMPLATE_ROOT="authentication/"
def getContext(request):
    context=CoreContext(request=request,app_name=APP_NAME)
    return context


def ProfileContext(request,*args, **kwargs):
    context=getContext(request=request)
    if 'profile' in kwargs:
        selected_profile=kwargs['profile']
    elif 'profile_id' in kwargs:
        selected_profile=ProfileRepo(request=request).profile(pk=kwargs['profile_id'])
    elif 'pk' in kwargs:
        selected_profile=ProfileRepo(request=request).profile(pk=kwargs['pk'])
    context['selected_profile']=selected_profile
    if request.user.has_perm(APP_NAME+".change_profile"):
        context['login_as_user_form']=LoginAsUserForm()

    return context


class BasicViews(View):
    def home(self,request,*args, **kwargs):
        context=getContext(request)
        return render(request,TEMPLATE_ROOT+"index.html",context)


class ProfileViews(View):
    def upload_profile_image(self,request,*args, **kwargs):
        profile_id=0
        if 'profile_id' in kwargs:
            profile_id=kwargs['profile_id']
        else:
            profile_id=ProfileRepo(request.user).me.id
        upload_profile_image_form=UploadProfileImageForm(request.POST,request.FILES)
        if upload_profile_image_form.is_valid():
            image=request.FILES['image']
            # profile_id=upload_profile_image_form.cleaned_data['profile_id']
            ProfileRepo(request=request).change_profile_image(profile_id=profile_id,image=image)                    
            return redirect(reverse(APP_NAME+":edit_profile_view",kwargs={'profile_id':profile_id}))
        return self.edit_profile(profile_id=profile_id,request=request)
    def edit_profile(self,request,*args, **kwargs):
        context=getContext(request)
        selected_profile=ProfileRepo(user=request.user).profile(*args, **kwargs)
        context['selected_profile']=selected_profile
        context['upload_profile_image_form']=UploadProfileImageForm()
        context['selected_profile_s']=json.dumps(ProfileSerializer(selected_profile).data)
        return render(request,TEMPLATE_ROOT+"edit-profile.html",context)
    def profile(self,request,*args, **kwargs):
        context=getContext(request)
        context['layout']="base-layout.html"
        selected_profile=ProfileRepo(user=request.user)
        if 'profile_id' in kwargs:
            selected_profile=ProfileRepo(request=request).profile(pk=kwargs['profile_id'])
        if 'pk' in kwargs:
            selected_profile=ProfileRepo(request=request).profile(pk=kwargs['pk'])
        context['selected_profile']=selected_profile
        return render(request,TEMPLATE_ROOT+"profile.html",context)
    def profile2(self,request,*args, **kwargs):
        context=getContext(request)
        context['layout']="base-layout.html"
        return render(request,TEMPLATE_ROOT+"profile2.html",context)


class AuthenticationViews(View):
    def login_as_user(self,request,*args, **kwargs):
        log=1
        if request.method=='POST':
            log=2
            login_as_user_form=LoginAsUserForm(request.POST)
            if login_as_user_form.is_valid():
                log=3
                username=login_as_user_form.cleaned_data['username']
                request=ProfileRepo(request=request).login_as_user(username=username)
                if request is not None:
                    log=4
                    return redirect(SITE_URL)
        return redirect("authentication:login")

    def profiles(self,request,*args, **kwargs):
        context=getContext(request)
        profiles=ProfileRepo(request=request).list()
        context['profiles']=profiles
        profiles_s=json.dumps(ProfileSerializer(profiles,many=True).data)
        context['profiles_s']=profiles_s
        return render(request,TEMPLATE_ROOT+"profiles.html",context)
    
    def login(self,request,*args, **kwargs):
        if request.method=='POST':
            login_form=LoginForm(request.POST)
            if login_form.is_valid():
                username=login_form.cleaned_data['username']

                password=login_form.cleaned_data['password']
                back_url=login_form.cleaned_data['back_url']
                if back_url is None or not back_url:
                    back_url=SITE_URL
                request1=ProfileRepo(user=None).login(request=request,username=username,password=password)
                if request1 is not None and request1.user is not None and request1.user.is_authenticated :
                    return redirect(back_url)
                else:   
                    context=getContext(request=request)
                    context['message']='نام کاربری و کلمه عبور صحیح نمی باشد.'
                    context['login_form']=LoginForm()
                    context['search_form']=None
                    context['back_url']=back_url
                    return render(request,TEMPLATE_ROOT+'login.html',context)
        else:
            context=getContext(request)
            back_url=request.GET.get('next','/')
            context['back_url']=back_url
            return render(request,TEMPLATE_ROOT+"login.html",context)
            
    def register(self,request,*args, **kwargs):
        context=getContext(request=request)
        if request.method=='POST':
            register_form=RegisterForm(request.POST)
            if register_form.is_valid():
                username=register_form.cleaned_data['username']
                first_name=register_form.cleaned_data['first_name']
                last_name=register_form.cleaned_data['last_name']
                # email=register_form.cleaned_data['email']
                email=""
                # address=register_form.cleaned_data['address']
                address=""
                mobile=register_form.cleaned_data['mobile']
                # bio=register_form.cleaned_data['bio']
                bio=""
                password=register_form.cleaned_data['password']
                (result,profile,message)=ProfileRepo(user=None).register(request=request,email=email,username=username,password=password,first_name=first_name,last_name=last_name,mobile=mobile,bio=bio,address=address)
                context['message']=message
                if result==FAILED :
                    context['search_form']=None
                    context['register_form']=RegisterForm()
                    return render(request,TEMPLATE_ROOT+'register.html',context)
                if result==SUCCEED:
                    ProfileRepo(user=None).login(request=request,username=username,password=password)
                    return redirect(profile.get_absolute_url())
        else:   
            context=getContext(request)
            return render(request,TEMPLATE_ROOT+"register.html",context)
    def reset_password(self,request,*args, **kwargs):
        context=getContext(request=request)
        if 'profile_id' in kwargs:
            profile_id=kwargs['profile_id']
            selected_profile=ProfileRepo(request=request).profile(profile_id=profile_id)
        else:
            selected_profile=ProfileRepo(request=request).me
        context['selected_profile']=selected_profile
        if request.method=='GET':
            context['reset_password_form']=ResetPasswordForm()
            return render(request,TEMPLATE_ROOT+"reset-password.html",context)

        if request.method=='POST':
            reset_password_form=ResetPasswordForm(request.POST)
            if reset_password_form.is_valid():
                username=reset_password_form.cleaned_data['username']
                old_password=reset_password_form.cleaned_data['old_password']
                new_password=reset_password_form.cleaned_data['new_password']
                
                (result,profile,request1,message)=ProfileRepo(request=request).reset_password(request=request,
                        username=username,
                        new_password=new_password,
                        old_password=old_password,
                        )
                if result==FAILED :
                    context['message']=message
                    context['search_form']=None
                    context['reset_password_form']=ResetPasswordForm()
                if result==SUCCEED:
                    # ProfileRepo(request=request).profile(username=username)
                    return redirect(profile.get_absolute_url())
        return render(request,TEMPLATE_ROOT+"reset-password.html",context)
    def logout(self,request):
        ProfileRepo.logout(request)
        return redirect(reverse('authentication:login'))