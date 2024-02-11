from django import forms
from django.contrib.auth.forms import PasswordResetForm


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100, error_messages={
                               'required': 'Please enter your username',
                               'max_length': 'Username must be less than 100 characters',
                               })
    password = forms.CharField(widget=forms.PasswordInput)

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label='Email', max_length=254)