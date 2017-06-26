from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import TemplateView, CreateView
from django.utils import timezone
from django.http import HttpResponse

from atcoder_ranking.commons.libraries import *

from .forms import RegisterForm, CreatePostsForm, LoginForm
from .models import *


class TopView(TemplateView):
    template_name = 'top.html'

    def get(self, _, *args, **kwargs):
        context = super(TopView, self).get_context_data(**kwargs)

        return render(self.request, self.template_name, context)


def plotResults(request):
    users = User.objects.all()
    results = Result.objects
    users_name_list = []
    python_score_list = []
    cpp_score_list = []
    others_score_list = []

    for user in User.objects.all():
        users_name_list.append(str(user))
        python_score_list = np.append(python_score_list,len(results.filter(user=user, result_language='Python')) * 100)
        cpp_score_list = np.append(cpp_score_list,len(results.filter(user=user, result_language='C++')) * 100)
        others_score_list = np.append(others_score_list,len(results.filter(user=user, result_language='Others')) * 100)

    fig = Figure()
    ax = fig.add_subplot(1, 1, 1)

    left = np.arange(len(users_name_list))

    p1 = ax.barh(left, others_score_list, color="blue")
    p2 = ax.barh(left, cpp_score_list, left=others_score_list, color="skyblue")
    p3 = ax.barh(left, python_score_list, left=cpp_score_list + others_score_list, color="lightblue")
    ax.legend((p1[0], p2[0], p3[0]), ("Others", "C++", "Python"))
    ax.set_xlabel('Score')
    ax.set_ylabel('Users')
    ax.set_yticklabels(users_name_list, fontdict=None, minor=False)
    canvas = FigureCanvas(fig)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)

    return response


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'
    def get(self, _, *args, **kwargs):
        users = User.objects.all()
        results = Result.objects.all().select_related('user')
        for user in users:
            user.score = len(results.filter(user=user)) * 100
            language_list = [result.result_language for result in results.filter(user=user)]
            if language_list != []:
                # もっとも数が多い言語を主言語として選択
                user.main_language = Counter(language_list).most_common(1)[0][0]
            user.save()

        context = super(IndexView, self).get_context_data(**kwargs)
        context['users'] = User.objects.all().order_by('-score')[: 3]

        return render(self.request, self.template_name, context)


class MyPageView(LoginRequiredMixin, TemplateView):
    template_name = 'mypage.html'

    def get(self, _, *args, **kwargs):
        context = super(MyPageView, self).get_context_data(**kwargs)
        user = self.request.user
        results = Result.objects.filter(user=user)
        score = len(results) * 100
        context['results'] = results
        context['score'] = score

        return render(self.request, self.template_name, context)


class CreateUserView(CreateView):
    template_name = 'create.html'
    form_class = RegisterForm

    def post(self, _, *args, **kwargs):
        form = self.form_class(self.request.POST)
        if not form.is_valid():
            return render(self.request, self.template_name, {'form': form})
        else:
            data = form.cleaned_data
            user = User(
                username=data['username'],
                arc_user_name=data['arc_user_name'],
                email=data['email'],
            )
            user.set_password(data['password'])
            user.save()

            return redirect('/ranking/users/')


class UsersView(LoginRequiredMixin, TemplateView):
    template_name = 'users.html'

    def get(self, _, *args, **kwargs):
        users = User.objects.all()
        context = super(UsersView, self).get_context_data(**kwargs)
        context['users'] = users

        return render(self.request, self.template_name, context)


class AtCoderProblemsView(LoginRequiredMixin, TemplateView):
    template_name = 'problems.html'

    def get(self, _, *args, **kwargs):
        context = super(AtCoderProblemsView, self).get_context_data(**kwargs)
        problems = AtCoderProblem.objects.all()
        context['problems'] = problems[::-1]

        return render(self.request, self.template_name, context)


class GetProblemsView(LoginRequiredMixin, TemplateView):
    model = AtCoderProblem, User

    def get(self, _, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return redirect('/ranking/problems/')

    def get_context_data(self,**kwargs):
        context = super(GetProblemsView, self).get_context_data(**kwargs)
        user = self.request.user
        problems = AtCoderProblem.objects.all()
        existing_contest_list = [str(problems[i])for i in range(len(problems))]
        #Get Contest Links
        atcoder_contest_archive_html = requests.get('https://atcoder.jp/contest/archive').text
        atcoder_contest_archive_soup = BeautifulSoup(atcoder_contest_archive_html, "html.parser")
        atcoder_contest_archive_list = atcoder_contest_archive_soup.find_all("a", text=re.compile("AtCoder"))
        atcoder_contest_archive = {lst.string: lst.get("href") for lst in atcoder_contest_archive_list}
        latest_contest_list = list(atcoder_contest_archive.keys())[:6]

        for contest in latest_contest_list:
            if contest not in existing_contest_list:
                #Get Tasks
                task_list_html = requests.get(atcoder_contest_archive[contest] + '/assignments').text
                task_list_soup = BeautifulSoup(task_list_html, "html.parser")
                task_list = task_list_soup.find_all("a", href=re.compile("/tasks"),)
                task_link_dict = {task.string: task.get('href') for task in task_list if len(task.string) == 1}
                tasks_dict = {}
                for task_name, task_link in task_link_dict.items():
                    task_html = requests.get(atcoder_contest_archive[contest] + task_link).text
                    task_soup = BeautifulSoup(task_html, "html.parser")
                    task_content = task_soup.find('section').text
                    tasks_dict.update({task_name : task_content})

                if "Regular" in contest:
                    problem = AtCoderProblem(
                        problem_name=contest,
                        task_c=tasks_dict['C'],
                        task_d=tasks_dict['D'],
                        task_e=tasks_dict['E'],
                        task_f=tasks_dict['F'],
                    )
                elif "Grand" in contest:
                    problem = AtCoderProblem(
                        problem_name=contest,
                        task_a=tasks_dict['A'],
                        task_b=tasks_dict['B'],
                        task_c=tasks_dict['C'],
                        task_d=tasks_dict['D'],
                        task_e=tasks_dict['E'],
                        task_f=tasks_dict['F'],
                    )
                else:
                    problem = AtCoderProblem(
                        problem_name=contest,
                        task_a=tasks_dict['A'],
                        task_b=tasks_dict['B'],
                        task_c=tasks_dict['C'],
                        task_d=tasks_dict['D'],
                    )
                problem.save()

            return context

class CreatePostsView(LoginRequiredMixin, TemplateView):
    template_name = 'create_posts.html'
    form_class = CreatePostsForm

    def post(self, _, *args, **kwargs):
        form = self.form_class(self.request.POST)
        if not form.is_valid():
            return render(self.request, self.template_name, {'form': form})
        else:
            now = timezone.now()
            data = form.cleaned_data
            result = Result(user=self.request.user,
                            result_problem=data['result_problem'],
                            result_language=data['result_language'],
                            result_coding_time=data['result_coding_time'],
                            result_running_time=data['result_running_time'],
                            pub_date=now,
                            result_code=data['result_code']
                            )
            result.save()

            return redirect('/ranking/posts/')

class PostsView(LoginRequiredMixin, TemplateView):
    template_name = 'posts.html'

    def get(self, _, *args, **kwargs):
        context = super(PostsView, self).get_context_data(**kwargs)
        results = Result.objects.all()
        context['results'] = results[::-1]
        return render(self.request, self.template_name, context)


class PostsDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'posts_detail.html'

    def get(self, _, posts_id, *args, **kwargs):
        context = super(PostsDetailView, self).get_context_data(**kwargs)
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
    form_class = LoginForm

    def get(self, _, *args, **kwargs):
        if self.request.user.is_authenticated():
            return redirect('/ranking/')
        else:
            form = self.form_class(self.request.POST)
            return render(self.request, self.template_name, {'form': form})

    def post(self, _, *args, **kwargs):
        form = self.form_class(self.request.POST)
        username = form['username']
        password = form['password']
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth_views.login(self.request, user)
            return redirect('/ranking/')
        else:
            kwargs = {'template_name': 'login.html'}
            return auth_views.login(self.request, *args, **kwargs)


def logout(request):
    context = {
        'template_name': 'logout.html',
    }
    return auth_views.logout(request, **context)
