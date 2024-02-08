from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100, error_messages={
                               'required': 'Please enter your username',
                               'max_length': 'Username must be less than 100 characters',
                               })
    password = forms.CharField(widget=forms.PasswordInput)
