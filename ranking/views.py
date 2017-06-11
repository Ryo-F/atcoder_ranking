from django.core.urlresolvers import reverse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from .models import User, Result
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView, CreateView
from django.core.urlresolvers import reverse_lazy

from .forms import RegisterForm, LoginForm

# Create your views here.


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'
    context_object_name = 'latest_rank'

    def get(self, request, *args, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        return render(self.request, self.template_name, context)


class TopView(TemplateView):
    template_name = 'top.html'
    context_object_name = 'latest_rank'

    def get(self, request, *args, **kwargs):
        context = super(TopView, self).get_context_data(**kwargs)

        return render(self.request, self.template_name, context)


class MyPageView(LoginRequiredMixin, TemplateView):
    template_name = 'mypage.html'
    context_object_name = 'latest_rank'

    def get(self, request, *args, **kwargs):
        context = super(MyPageView, self).get_context_data(**kwargs)
        return render(self.request, self.template_name, context)


class CreateUserView(CreateView):
    template_name = 'create.html'
    form_class = RegisterForm
    success_url = reverse_lazy('top')


def login(request):
    context = {
        'template_name': 'login.html',
        'authentication_form': LoginForm
    }
    return auth_views.login(request, **context)


def logout(request):
    context = {
        'template_name': 'top.html',
    }
    return auth_views.logout(request, **context)
