from django import forms

class AddFeederForm(forms.Form):
    feeder_id=forms.IntegerField(required=True)

class GetBusDataForm(forms.Form):
    bus_id=forms.IntegerField(required=True)

class ReadComServerForm(forms.Form):
    com_server_id=forms.IntegerField( required=True)
    address=forms.IntegerField( required=False)
    count=forms.IntegerField( required=False)
    
class ReadForm(forms.Form):
    com_server_id=forms.IntegerField(required=True)

class WriteCommandForm(forms.Form):
    host=forms.CharField(max_length=50,required=True)
    port=forms.IntegerField( required=True)
    address=forms.IntegerField(required=True)
    value=forms.IntegerField(required=True)
    # value=forms.CharField(max_length=50,required=True)

class ReadCommandForm(forms.Form):
    host=forms.CharField(max_length=50,required=True)
    port=forms.IntegerField( required=True)
    address=forms.IntegerField(required=True)
    # value=forms.CharField(max_length=50,required=True)

class GetAnalogDataForm(forms.Form):
    host=forms.CharField(max_length=50,required=True)
    port=forms.IntegerField( required=True)
    address=forms.IntegerField( required=True)
    count=forms.IntegerField(required=True)

class AddComServerForm(forms.Form):
    name=forms.CharField(max_length=50, required=True)

class AddInputCommandForm(forms.Form):
    input_id=forms.CharField(max_length=50, required=True)
    command=forms.BooleanField(required=True)

class ReadCircuitBreakerForm(forms.Form):
    cb_id=forms.IntegerField(required=True)

class ToggleCircuitBreakerForm(forms.Form):
    cb_id=forms.IntegerField(required=True)
    command=forms.CharField(max_length=50,required=False)

class GetFeederForm(forms.Form):
    feeder_id=forms.IntegerField(required=True)