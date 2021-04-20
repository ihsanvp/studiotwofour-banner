from django.core.exceptions import ValidationError
from client.models import Client
from django import forms
from .models import Campaign

def validate_zip(value) :
  
  if not str(value).endswith('.zip') :
    raise ValidationError('must be zip file')
  else :
    return value

class CampaignForm(forms.ModelForm) :
  class Meta :
    model = Campaign
    fields = '__all__'


class UploadBundleForm(forms.Form) :
  file = forms.FileField(help_text='Must be .zip file', validators=[validate_zip])
  client = forms.ModelChoiceField(queryset=Client.objects.all())


