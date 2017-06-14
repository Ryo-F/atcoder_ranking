from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = (
            "username", "email", "password1", "password2",
            "first_name", "last_name",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'ユーザ名'

        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'メールアドレス'

        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['placeholder'] = '姓'

        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['placeholder'] = '名'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'パスワード'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'パスワード（確認）'


class CreatePostsForm(forms.ModelForm):
    result_problem = forms.CharField()
    result_language = forms.CharField()
    result_coding_time = forms.IntegerField()
    result_running_time = forms.IntegerField()
    pub_date = forms.DateTimeField('date published')
    result_code = forms.CharField(
        widget=forms.Textarea, max_length=500, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['result_problem'].widget.attrs['class'] = 'form-control'
        self.fields['result_problem'].widget.attrs['placeholder'] = 'Problem'

        self.fields['result_language'].widget.attrs['class'] = 'form-control'
        self.fields['result_language'].widget.attrs['placeholder'] = 'Language'

        self.fields['result_coding_time'].widget.attrs['class'] = 'form-control'
        self.fields['result_coding_time'].widget.attrs['placeholder'] = 'Coding_Time'

        self.fields['result_running_time'].widget.attrs['class'] = 'form-control'
        self.fields['result_running_time'].widget.attrs['placeholder'] = 'Running_Time'

        self.fields['pub_date'].widget.attrs['class'] = 'form-control'

        self.fields['result_code'].widget.attrs['class'] = 'form-control'
        self.fields['result_code'].widget.attrs['class'] = 'Code'


class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'ユーザ名'

        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'パスワード'
