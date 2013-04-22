from django.db import models
from django import forms
from evmev.ilan.models import ilan

class ilanForm(forms.ModelForm):
	name = 'Ilan Formu'
	class Meta:
	        model = ilan

class ContactForm(forms.Form):
	subject = forms.CharField(max_length=100)
	sender = forms.EmailField()
	message = forms.CharField(widget=forms.Textarea)
    


