from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label='ユーザーネーム', max_length=100)
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput)