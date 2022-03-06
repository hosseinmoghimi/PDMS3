from django.http.response import Http404, JsonResponse
from .mail import send_mail
from rest_framework.views import APIView
from core.constants import SUCCEED,FAILED
from .forms import SendEmailForm
class BasicApis(APIView):
    def send_mail(self,request,*args, **kwargs):
        context={'result':FAILED}
        log=1
        if request.method=='POST':
            log=2
            send_email_form=SendEmailForm(request.POST)
            if send_email_form.is_valid():
                log=3
                cd=send_email_form.cleaned_data
                subject=cd['subject']
                receiver_email=cd['receiver_email']
                message=cd['message']
                (result,message)=send_mail(subject=subject,receiver_email=receiver_email,message=message)
                if result==SUCCEED:
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)