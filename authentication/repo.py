from django.core.checks import messages
from core.constants import FAILED, SUCCEED
from .models import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User

class ProfileRepo():
    def __init__(self,*args, **kwargs):
        self.request=None
        self.me=None
        self.objects=None   
        self.user=None
        self.app_name=None
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        if 'user' in kwargs:
            self.user=kwargs['user']
        if 'forced' in kwargs:
            self.objects = Profile.objects.all()
        elif self.user is not None and self.user and self.user.is_authenticated:
            self.objects = Profile.objects.filter(enabled=True)
            self.me = self.objects.filter(user=self.user).first()         
        self.objects = Profile.objects.filter(enabled=True)

    def reset_password(self,*args, **kwargs):
        result=FAILED
        message=""
        profile=None
        username=""
        old_password=""
        new_password=""
        request=None
        if 'request' in kwargs:
            request=kwargs['request']
        if 'username' in kwargs:
            username=kwargs['username']
        if 'old_password' in kwargs:
            old_password=kwargs['old_password']
        if 'new_password' in kwargs:
            new_password=kwargs['new_password']
            
        selected_user=User.objects.filter(username=username).first()
        
        if selected_user is None :            
            result=FAILED
            profile=None
            message="چنین کاربری وجود ندارد."
            return (result,profile,request,message)

    
        if self.user.has_perm(APP_NAME+".change_profile"):
            selected_user.set_password(new_password)
            selected_user.save()
            request=self.login(request=request,username=username,password=new_password)
            result=SUCCEED
            profile=Profile.objects.filter(user=selected_user).first()
            message="کلمه عبور با موفقیت تغییر یافت."
            return (result,profile,request,message)

        selected_user=authenticate(request=request,username=username,password=old_password)  
        if selected_user is not None:
            selected_user.set_password(new_password)
            selected_user.save()
            if selected_user is not None:
                request=authenticate(request=request,username=username,password=new_password)
                result=SUCCEED
                profile=Profile.objects.filter(user=selected_user).first()
                message="کلمه عبور با موفقیت تغییر یافت."
                return (result,profile,request,message)
        
        message="ناموفق"
        return (result,profile,request,message)
    def change_profile_image(self,profile_id,image):
        profile=self.profile(profile_id=profile_id)
        if profile is not None:
            profile.image_origin = image
            profile.save()
            return True
        return False
       
    def profile(self,*args, **kwargs):
        pk=0
        if 'profile_id' in kwargs:
            pk=kwargs['profile_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        elif 'username' in kwargs:
            username=kwargs['username']
            return Profile.objects.filter(user__username=username).first()
        return self.objects.filter(pk=pk).first()

    @classmethod
    def logout(self,request):
        logout(request=request)

    def login(self,request,username,password):
        user=authenticate(request=request,username=username,password=password)
        if user is not None:
            login(request,user)
            if user.is_authenticated:
                return request
        return None
    def login_as_user(self,username):
        if not self.user.has_perm(APP_NAME+".change_profile"):
            return
        user=User.objects.filter(username=username).first()
        if user is None:
            return None
        login(request=self.request,user=user,backend='django.contrib.auth.backends.ModelBackend')
        return self.request
        
    def list(self,*args, **kwargs):
        if self.user.has_perm(APP_NAME+".view_profile"):
            return Profile.objects.all()
        return Profile.objects.filter(pk=0)
    

    def edit_profile(self,*args, **kwargs):
        profile_id=0
        if 'profile_id' in kwargs:
            profile_id=kwargs['profile_id']
        if not self.user.has_perm(APP_NAME+".change_profile") and not self.me.id==profile_id:
            return False

        edited_profile=Profile.objects.get(pk=profile_id)
        
        edited_user=edited_profile.user
        # first_name=""
        # last_name=""
        # mobile=""
        # slogan=""
        # address=""
        # bio=""
        if 'first_name' in kwargs:
            edited_user.first_name=kwargs['first_name']
            first_name=kwargs['first_name']
        if 'last_name' in kwargs:
            edited_user.last_name=kwargs['last_name']
            last_name=kwargs['last_name']
        if 'email' in kwargs:
            edited_user.email=kwargs['email']
            email=kwargs['email']
        if 'bio' in kwargs:
            edited_profile.bio=kwargs['bio']
            bio=kwargs['bio']
        if 'mobile' in kwargs:
            edited_profile.mobile=kwargs['mobile']
            mobile=kwargs['mobile']
        if 'address' in kwargs:
            edited_profile.address=kwargs['address']
            address=kwargs['address']
        
        edited_user.save()
        edited_profile.save()
        return True

        user=self.user
        if user.is_authenticated:
            me=ProfileRepo(user=user).me
            if me.id==profile_id or me.user.has_perm(APP_NAME+'.change_profile'):
                edited_profile=self.objects.get(pk=profile_id)
                edited_profile=self.objects.get(pk=profile_id)
                
                if edited_profile is not None:
                    if edited_profile.user is not None:
                        edited_profile.user.first_name=first_name
                        edited_profile.user.last_name=last_name
                        edited_profile.user.save()


                    edited_profile.first_name=first_name
                    edited_profile.last_name=last_name
                    edited_profile.mobile=mobile
                    edited_profile.slogan=slogan
                    edited_profile.bio=bio
                    edited_profile.address=address
                    edited_profile.postal_code=postal_code
                    
                    edited_profile.save()
                    return edited_profile
        return None
    

    def register(self,*args, **kwargs):
        # if not self.user.has_perm(APP_NAME+".add_profile"):
        #     return (FAILED,None,"")

        from django.contrib.auth.models import User
        username=""
        password=""
        email=""
        last_name=""
        first_name=""
        if 'username' in kwargs:
            username=kwargs['username']
        if 'password' in kwargs:
            password=kwargs['password']
        if 'email' in kwargs:
            email=kwargs['email']
        if 'last_name' in kwargs:
            last_name=kwargs['last_name']
        if 'first_name' in kwargs:
            first_name=kwargs['first_name']
        if len(User.objects.filter(username=username))>0:
            return (FAILED,None,"نام کاربری تکراری")
        profile=Profile()
        user=User.objects.create(username=username,first_name=first_name,last_name=last_name,email=email)
        user.set_password(password)
        user.save()
        profile=Profile.objects.filter(user=user).first()
        if profile is None:
            profile=Profile(user=user)
        if 'bio' in kwargs:
            profile.bio=kwargs['bio']
        if 'mobile' in kwargs:
            profile.mobile=kwargs['mobile']
        if 'address' in kwargs:
            profile.address=kwargs['address']
        profile.save()
        result=SUCCEED
        message="successfully!"
        return (result,profile,message)