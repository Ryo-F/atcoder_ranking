from django.core.urlresolvers import reverse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from .models import User, Result
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView, CreateView
from django.core.urlresolvers import reverse_lazy

from .forms import RegisterForm, CreatePostsForm, LoginForm

# Create your views here.


class TopView(TemplateView):
    template_name = 'top.html'

    def get(self, request, *args, **kwargs):
        context = super(TopView, self).get_context_data(**kwargs)

        return render(self.request, self.template_name, context)


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        return render(self.request, self.template_name, context)


class MyPageView(LoginRequiredMixin, TemplateView):
    template_name = 'mypage.html'

    def get(self, request, *args, **kwargs):
        context = super(MyPageView, self).get_context_data(**kwargs)
        current_user = request.user.id
        print(current_user)
        results = Result.objects.prefetch_related()
        context['results'] = results
        context['current_user'] = current_user
        return render(self.request, self.template_name, context)


class CreateUserView(CreateView):
    template_name = 'create.html'
    form_class = RegisterForm
    success_url = '/ranking/'


class UsersView(LoginRequiredMixin, TemplateView):
    template_name = 'users.html'
    context_object_name = 'latest_rank'

    def get(self, request, *args, **kwargs):
        context = super(UsersView, self).get_context_data(**kwargs)
        return render(self.request, self.template_name, context)


class ProblemsView(LoginRequiredMixin, TemplateView):
    template_name = 'problems.html'
    context_object_name = 'latest_rank'

    def get(self, request, *args, **kwargs):
        context = super(ProblemsView, self).get_context_data(**kwargs)
        return render(self.request, self.template_name, context)


class CreatePostsView(LoginRequiredMixin, TemplateView):
    template_name = 'create_posts.html'
    form_class = CreatePostsForm
    initial = [
        {'result_problem': 'AtCoder Beginner Contest 064'},
        {'result_language': 'Python'},
        {'result_code': 'Code'}
    ]

    def get(self, request, *args, **kwargs):
        context = super(CreatePostsView, self).get_context_data(**kwargs)
        results = Result.objects.prefetch_related()
        context['results'] = results
        return render(self.request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            package = Package.objects.create(result_problem=data['result_problem'],
                                             result_language=data['result_language'],
                                             result_coding_time=data['result_coding_time'],
                                             result_running_time=data['result_running_time'],
                                             pub_date=data['pub_date'],
                                             result_code=data['result_code']
                                             )
        return render(self.request, self.template_name, {'form': form})


class PostsView(LoginRequiredMixin, TemplateView):
    template_name = 'posts.html'

    def get(self, request, *args, **kwargs):
        context = super(PostsView, self).get_context_data(**kwargs)
        results = Result.objects.prefetch_related()
        context['results'] = results
        return render(self.request, self.template_name, context)


class PostsDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'posts_detail.html'

    def get(self, request, posts_id, *args, **kwargs):
        context = super(PostsDetailView, self).get_context_data(**kwargs)
        # results = Result.objects.prefetch_related()
        result = get_object_or_404(Result, pk=posts_id)
        context['result'] = result
        return render(self.request, self.template_name, context)


def login(request):
    context = {
        'template_name': 'login.html',
        'authentication_form': LoginForm
    }
    return auth_views.login(request, **context)


def logout(request):
    context = {
        'template_name': 'logout.html',
    }
    return auth_views.logout(request, **context)
