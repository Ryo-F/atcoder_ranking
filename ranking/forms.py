from django import forms
# from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import *


class RegisterForm(forms.ModelForm):

    class Meta:
        model = User
        fields = (
            "username", "email", "arc_user_name", "password"
        )
        widgets = {
            'email': forms.EmailInput(),
            'password': forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'ユーザ名'

        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'メールアドレス'

        self.fields['arc_user_name'].widget.attrs['class'] = 'form-control'
        self.fields['arc_user_name'].widget.attrs['placeholder'] = 'AtCoderUserName'

        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'パスワード'


class CreatePostsForm(forms.ModelForm):

    class Meta:
        model = Result
        fields = (
            "result_problem", "result_language", "result_coding_time", "result_running_time",
            "result_code"
        )
        widgets = {
            'result_language': forms.Select,
            'result_code': forms.Textarea,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['result_problem'].widget.attrs['class'] = 'form-control'

        self.fields['result_language'].widget.attrs['class'] = 'form-control'
        self.fields['result_language'].widget.attrs['placeholder'] = 'Language'

        self.fields['result_coding_time'].widget.attrs['class'] = 'form-control'
        self.fields['result_coding_time'].widget.attrs['placeholder'] = 'Coding_Time'

        self.fields['result_running_time'].widget.attrs['class'] = 'form-control'
        self.fields['result_running_time'].widget.attrs['placeholder'] = 'Running_Time'

        self.fields['result_code'].widget.attrs['class'] = 'form-control'
        self.fields['result_code'].widget.attrs['placeholder'] = 'Code'


class CreateProblemForm(forms.ModelForm):
    PROBLEM_CHOICES = (
        (1, 'ABC'),
        (2, 'ARC'),
        (3, 'AGC')
    )
    problem_name = forms.ChoiceField(
        widget=forms.Select, choices=PROBLEM_CHOICES)
    problem_num = forms.CharField(max_length='3')


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "password")
        widgets = {'password': forms.PasswordInput(), }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'ユーザ名'

        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'パスワード'
