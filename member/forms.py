from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(label="이메일", widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': '이메일을 입력해 주세요.'
    }))
    password = forms.CharField(label="비밀번호", widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': '비밀번호를 입력해 주세요.'
    }))