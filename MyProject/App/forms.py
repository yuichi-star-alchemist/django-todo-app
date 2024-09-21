from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.core.exceptions import ValidationError

from .models import AppUsers, Tasks


class EmailLoginForm(AuthenticationForm):
    username = UsernameField(
        label='',# レンダリング時のlabel名 空ならlabel自体生成されない
        widget=forms.EmailInput(
            attrs={'id': 'email','placeholder': 'メールアドレス','maxlength': 64}
        )
    )
    password = forms.CharField(
        label='',
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password",'placeholder': 'パスワード'}
        )
    )

    error_messages = {
        "invalid_login": "メールアドレスまたはパスワードに誤りがあります",
        "inactive": 'このアカウントは非アクティブです',
    }
    # これ上でできそうですね・・
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['autocomplete'] = 'email'


class UserForm(forms.ModelForm):
    password_confirm = forms.CharField(
        label='',
        max_length=128,
        widget=forms.PasswordInput(
            attrs={'placeholder': 'パスワード確認'}
        )
    )
    
    class Meta:
        model = AppUsers
        fields = ['email', 'username', 'password']
        widgets = {# 生成されるhtml要素への変更
            'email': forms.EmailInput(attrs={'placeholder': 'メールアドレス'}),
            'username': forms.TextInput(attrs={'placeholder': 'ユーザー名'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'パスワード'})
        }
    # これもうえでできそう・・
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label = ''
        # self.label_suffix = ''
    
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
            'detail': forms.Textarea(attrs={'rows': 5, 'cols': 24}),
            'end_time': forms.DateInput(attrs={'type': 'date'}),
        }
    # これも上でできそう
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''