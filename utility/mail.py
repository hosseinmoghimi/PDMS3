from core.constants import FAILED, SUCCEED
from pdms.settings import EMAIL_PORT,EMAIL_HOST_USER,EMAIL_HOST_PASSWORD,EMAIL_HOST
from django.core.mail import send_mail as send_mail_origin
import smtplib, ssl
from pdms.settings import SEND_EMAIL

def send_mail(*args, **kwargs):
    result=FAILED
    message=""

    if not SEND_EMAIL:
        return (result,message)
    subject = kwargs['subject'] if 'subject' in kwargs else None
    message = kwargs['message'] if 'message' in kwargs else None
    from_ = EMAIL_HOST_USER
    receiver_email = kwargs['receiver_email'] if 'receiver_email' in kwargs else None
    return send_mail_origin(
        subject,
        message,
        from_,
        [receiver_email],
        fail_silently=False,
    )



# def send_mail2(*args, **kwargs):
#     subject = kwargs['subject'] if 'subject' in kwargs else None
#     message = kwargs['message'] if 'message' in kwargs else None
#     from_ = kwargs['from_'] if 'from_' in kwargs else None
#     to_ = kwargs['to_'] if 'to_' in kwargs else None
  
#     import smtplib, ssl
#     port = 465  # For SSL
#     password = input("Type your password and press enter: ")

#     # Create a secure SSL context
#     context = ssl.create_default_context()

#     with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT, context=context) as server:
#         server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)


def send_mail3(*args, **kwargs):
    result=FAILED
    message=""

    if not SEND_EMAIL:
        return (result,message)
    # Create a secure SSL context
    context = ssl.create_default_context()

    # Try to log in to server and send email
    try:
        server = smtplib.SMTP(EMAIL_HOST,EMAIL_PORT)
        server.ehlo() # Can be omitted
        server.starttls(context=context) # Secure the connection
        server.ehlo() # Can be omitted
        server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        server.connect(host=EMAIL_HOST,port=EMAIL_PORT)
        a=server.sendmail(from_addr=EMAIL_HOST_USER,to_addrs=kwargs['receiver_email'], msg=kwargs['message'])
        result=SUCCEED
        message="ارسال پیام با موفقیت انجام شد."

    except Exception as e:
        # Print any error messages to stdout
        # print(e)
        pass
    finally:
        server.quit() 
        return (result,message)