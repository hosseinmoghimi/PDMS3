from django import forms


class SendEmailForm(forms.Form):
    subject=forms.CharField(max_length=100, required=True)
    receiver_email=forms.CharField(max_length=100, required=True)
    message=forms.CharField(max_length=100, required=True)