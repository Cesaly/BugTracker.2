from django.forms import ModelForm
from django import forms
from .models import Ticket


class Ticketadd(ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description']


class Login(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)


class Edit(ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'ticket_status', 'ticket_person']


class Adduser(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30)
