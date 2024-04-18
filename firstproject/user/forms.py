from django import forms
from .models import User,verify
from django.contrib.auth.forms import UserCreationForm

class UserSignupForm(UserCreationForm):
    email = forms.EmailField()
    phone = forms.CharField(max_length = 20)
    username = forms.CharField(max_length = 20)
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password']

class UserLoginForm(UserCreationForm):
    email = forms.EmailField()
    password= forms.CharField(max_length = 20)
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password']

class UserVerifyForm(UserCreationForm):
    verification_code = forms.CharField(max_length = 20)
    email=forms.EmailField(max_length=20)
    class Meta:
        model = verify
        fields = ['email', 'verification_code']

class UserPasswordForm(UserCreationForm):
    password = forms.CharField(max_length = 20)
    username = forms.CharField(max_length = 20)
    class Meta:
        model = User
        fields = ['username', 'password']