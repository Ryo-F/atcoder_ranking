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


'''
class CustomForm(forms.Form):
    error_messages = {'required': 'この項目は必須です', 'invalid': '有効な値を入力してください'}

    def __init__(self, *args, **kwargs):
        super(CustomForm, self).__init__(*args, **kwargs)

        for field in list(self.fields.values()):
            field.error_messages = self.error_messages


class CreatePostsForm(CustomForm):
    LANGUAGE_CHOICES = (
        (1, 'Python'),
        (2, 'C++'),
        (3, 'Others')
    )
    result_problem = forms.ModelChoiceField(AtCoderProblem.objects.all())
    result_language = forms.ChoiceField(
        widget=forms.Select, choices=LANGUAGE_CHOICES)
    result_coding_time = forms.IntegerField()
    result_running_time = forms.IntegerField()
    pub_date = forms.DateTimeField('date published')
    result_code = forms.CharField(
        widget=forms.Textarea, max_length=500, required=False)

    def clean_result_problem(self):
        if 'result_problem' not in self.cleaned_data:
            raise forms.ValidationError("problemを選択してください")
        return self.cleaned_data.get('result_problem')

    def clean(self):
        self.clean_result_problem()
        return super(CreatePostsForm, self).clean()
'''


class CreateProblemForm(forms.ModelForm):
    PROBLEM_CHOICES = (
        (1, 'ABC'),
        (2, 'ARC'),
        (3, 'AGC')
    )
    problem_name = forms.ChoiceField(
        widget=forms.Select, choices=PROBLEM_CHOICES)
    problem_num = forms.CharField(max_length='3')


class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'ユーザ名'

        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'パスワード'
