from django import forms


from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100, error_messages={
                               'required': 'Please enter your username',
                               'max_length': 'Username must be less than 100 characters',
                               })
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(label='First Name', max_length=100, required=False)
    last_name = forms.CharField(label='Last Name', max_length=100, required=False)
    user_photo = forms.ImageField(required=False)
    age = forms.IntegerField(label='Age', required=False)
    gender = forms.ChoiceField(label='Gender', choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], required=False)


