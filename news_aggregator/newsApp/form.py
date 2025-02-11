from django import forms
from django.contrib.auth.models import User
from .models import UserModel

class UserForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['email', 'password', 'username']
        labels = {
            'username': 'Username',
            'email': 'Email',
            'password': 'Password'
        }
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'username','class': 'form-control mb-4'}),
            'email': forms.EmailInput(attrs={'placeholder': 'your email','class': 'form-control mb-4'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'strong password','class': 'form-control mb-4'})
        }