from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.core.exceptions import ValidationError

from .models import AppUsers, Tasks


class EmailLoginForm(AuthenticationForm):
    username = UsernameField(
        label='メールアドレス',
        widget=forms.EmailInput(
            attrs={'id': 'email','placeholder': 'メールアドレス','maxlength': 64}
        )
    )
    password = forms.CharField(
        label='パスワード',
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password",'placeholder': 'パスワード'}
        )
    )

    error_messages = {
        "invalid_login": "メールアドレスまたはパスワードに誤りがあります",
        "inactive": 'このアカウントは非アクティブです',
    }
    
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['autocomplete'] = 'email'


class UserForm(forms.ModelForm):
    password_confirm = forms.CharField(widget=forms.PasswordInput, max_length=128, label='パスワード確認')
    
    class Meta:
        model = AppUsers
        fields = ['email', 'username', 'password']
        widgets = {'password': forms.PasswordInput}
    
    def clean(self):
        cleaned_data = super().clean()
        # パスワード一致確認
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise ValidationError('パスワードが一致しません')

        return cleaned_data


class TaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['title', 'detail', 'end_time']
        widgets = {
            'end_time': forms.DateInput(attrs={'type': 'date'})
        }