from django import forms
from django.core import validators

def checkbot(value):
    if len(value) != 0:
        raise forms.ValidationError("Plz try Again later")

class get_data(forms.Form):
    display_name = forms.CharField(widget=forms.TextInput(attrs={'name':'display_name', 'id':'display_name', 'placeholder':'Enter Your Display Name', 'required':''}))
    osm_username = forms.CharField(required=False ,widget=forms.TextInput(attrs={'name':'osm_username', 'id':'osm_username', 'placeholder':'osm username'}))
    mw_username = forms.CharField(required=False, widget=forms.TextInput(attrs={'name':'mw_username', 'id':'mw_username', 'placeholder':'media wiki username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'name':'email', 'id':'email', 'placeholder':'Your Email Address', 'required':'None'}))
    botcheck = forms.CharField(required=False, widget=forms.HiddenInput(), validators=[checkbot])