from django.core.urlresolvers import reverse
from django.template import loader
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView, CreateView
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate


from atcoder_ranking.commons import *

from .forms import RegisterForm, CreatePostsForm, LoginForm
from .models import *


class TopView(TemplateView):
    template_name = 'top.html'

    def get(self, request, *args, **kwargs):
        context = super(TopView, self).get_context_data(**kwargs)

        return render(self.request, self.template_name, context)


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        results = Result.objects.prefetch_related()
        context['results'] = results
        return render(self.request, self.template_name, context)


class MyPageView(LoginRequiredMixin, TemplateView):
    template_name = 'mypage.html'

    def get(self, request, *args, **kwargs):
        context = super(MyPageView, self).get_context_data(**kwargs)
        current_user = request.user.id
        results = Result.objects.prefetch_related()
        context['results'] = results
        context['current_user'] = current_user
        return render(self.request, self.template_name, context)


class CreateUserView(CreateView):
    template_name = 'create.html'
    form_class = RegisterForm
    success_url = '/ranking/'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User(
                username=data['username'],
                arc_user_name=data['arc_user_name'],
                email=data['email'],
                password=data['password']
            )
            user.save()
            print("saved")
        return render(self.request, self.template_name, {'form': form})


class UsersView(LoginRequiredMixin, TemplateView):
    template_name = 'users.html'
    model = User

    def get(self, request, *args, **kwargs):
        context = super(UsersView, self).get_context_data(**kwargs)
        users = User.objects.all()
        context['users'] = users
        return render(self.request, self.template_name, context)


class AtCoderProblemsView(LoginRequiredMixin, TemplateView):
    template_name = 'problems.html'
    model = AtCoderProblem

    def get(self, request, *args, **kwargs):
        context = super(AtCoderProblemsView, self).get_context_data(**kwargs)
        problems = AtCoderProblem.objects.prefetch_related()
        context['problems'] = problems
        return render(self.request, self.template_name, context)


class GetProblemsView(LoginRequiredMixin, TemplateView):
    model = AtCoderProblem, User

    def get(self, request, *args, **kwargs):
        context = super(GetProblemsView, self).get_context_data(**kwargs)

        def get_soup(url):
            html = requests.get(url).text
            return BeautifulSoup(html, "html.parser")

        def get_contest_links(url):
            html = requests.get(url).text
            soup = BeautifulSoup(html, "html.parser")
            lsts = soup.find_all("a", text=re.compile("AtCoder"))
            return{lst.string: lst.get("href") for lst in lsts}

        def get_tasks(contest):
            def get_task_content(task_link):
                soup = get_soup(atcoder_contest_archive[contest] + task_link)
                return soup.find('section').text
            url = atcoder_contest_archive[contest] + '/assignments'
            soup = get_soup(url)
            task_list = soup.find_all("a", href=re.compile("/tasks"),)
            link_dict = {task.string: task.get(
                'href') for task in task_list if len(task.string) == 1}
            return {key: get_task_content(value) for key, value in link_dict.items()}

        current_user = request.user.id
        atcoder_contest_archive = get_contest_links(
            'https://atcoder.jp/contest/archive')
        contest_list = list(atcoder_contest_archive.keys())[:5]
        for contest in contest_list:
            if "Regular" in contest:
                tasks_dict = get_tasks(contest)
                problem = AtCoderProblem(
                    problem_name=contest,
                    task_a=tasks_dict['C'],
                    task_b=tasks_dict['D'],
                    task_c=tasks_dict['E'],
                    task_d=tasks_dict['F'],
                )
            elif "Grand" in contest:
                tasks_dict = get_tasks(contest)
                problem = AGCProblem(
                    problem_name=contest,
                    task_a=tasks_dict['A'],
                    task_b=tasks_dict['B'],
                    task_c=tasks_dict['C'],
                    task_d=tasks_dict['D'],
                    task_e=tasks_dict['E'],
                    task_f=tasks_dict['F'],
                )
            else:
                tasks_dict = get_tasks(contest)
                problem = AtCoderProblem(
                    problem_name=contest,
                    task_a=tasks_dict['A'],
                    task_b=tasks_dict['B'],
                    task_c=tasks_dict['C'],
                    task_d=tasks_dict['D'],
                )
            problem.save()
        return HttpResponseRedirect('/ranking/problems/')


class CreatePostsView(LoginRequiredMixin, CreateView):
    template_name = 'create_posts.html'
    model = Result
    form_class = CreatePostsForm
    initial = {'result_problem': 'AtCoder Beginner Contest 064',
               'result_language': 'Python', }
    success_url = '/ranking/posts/'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        current_user = request.user.id

        # if form.is_valid():
        data = form.cleaned_data
        result = Result(user=User(id='current_user'),
                        result_problem=data['result_problem'],
                        result_language=data['result_language'],
                        result_coding_time=data['result_coding_time'],
                        result_running_time=data['result_running_time'],
                        pub_date=data['pub_date'],
                        result_code=data['result_code']
                        )
        result.save()
        print("saved")
        return render(self.request, self.template_name, {'form': form})


class PostsView(LoginRequiredMixin, TemplateView):
    template_name = 'posts.html'

    def get(self, request, *args, **kwargs):
        context = super(PostsView, self).get_context_data(**kwargs)
        results = Result.objects.all()
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


class LoginView(TemplateView):
    template_name = "login.html"

    def get(self, _, *args, **kwargs):
        if self.request.user.is_authenticated():
            return redirect(self.get_next_redirect_url())
        else:
            kwargs = {'template_name': 'login.html'}
            return auth_views.login(self.request, *args, **kwargs)

    def post(self, _, *args, **kwargs):
        username = self.request.POST['username']
        password = self.request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth_views.login(self.request, user)
            return redirect(self.get_next_redirect_url())
        else:
            kwargs = {'template_name': 'login.html'}
            return auth_views.login(self.request, *args, **kwargs)

    def get_next_redirect_url(self):
        redirect_url = self.request.GET.get('next')
        if not redirect_url or redirect_url == '/':
            redirect_url = '/ranking/'

        return redirect_url


def logout(request):
    context = {
        'template_name': 'logout.html',
    }
    return auth_views.logout(request, **context)
