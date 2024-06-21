from django import forms
from django.contrib.auth.models import User
from .models import Employee
from django.contrib.auth.hashers import make_password

class RegisterForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100, error_messages={
                               'required': 'Please enter your username',
                               'max_length': 'Username must be less than 100 characters',
                               })
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(label='First Name', max_length=100,)
    last_name = forms.CharField(label='Last Name', max_length=100, required=False)
    user_photo = forms.ImageField(required=False)
    age = forms.IntegerField(label='Age', required=False)
    gender = forms.ChoiceField(label='Gender', choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], required=False)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken. Please choose a different one.")
        return username

class ChangePasswordForm(forms.ModelForm):
    new_password = forms.CharField(label='New Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['new_password']

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and new_password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data['new_password'])
        if commit:
            user.save()
        return user

class UserEmployeeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['user_photo', 'age', 'gender']
    
    def clean_user_photo(self):
        user_photo = self.cleaned_data.get('user_photo')
        print("Cleaned data:", user_photo)
        if not user_photo:
            print("User photo cleared, returning None.")
            # If user photo is cleared, return None to delete the old image
            return None
        return user_photo