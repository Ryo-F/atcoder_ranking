from django.core.urlresolvers import reverse
from django.template import loader
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView, CreateView
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate
from django.utils import timezone
from django.http import HttpResponse

from atcoder_ranking.commons.libraries import *
from .forms import RegisterForm, CreatePostsForm, LoginForm
from .models import *


class TopView(TemplateView):
    template_name = 'top.html'

    def get(self, request, *args, **kwargs):
        context = super(TopView, self).get_context_data(**kwargs)

        return render(self.request, self.template_name, context)


def plotResults(request):
    users = User.objects
    results = Result.objects
    users_list = []
    python_len_list = np.array([])
    cpp_len_list = np.array([])
    others_len_list = np.array([])
    for user in users.all():
        users_list.append(str(user))
        python_len_list = np.append(python_len_list,
                                    len(results.filter(user=user, result_language='Python')) * 100)
        cpp_len_list = np.append(cpp_len_list,
                                 len(results.filter(user=user, result_language='C++')) * 100)
        others_len_list = np.append(others_len_list,
                                    len(results.filter(user=user, result_language='Others')) * 100)
    fig = Figure()
    ax = fig.add_subplot(1, 1, 1)

    left = np.arange(len(users_list))

    p1 = ax.barh(left, others_len_list, color="blue")
    p2 = ax.barh(left, cpp_len_list,
                 left=others_len_list, color="skyblue")
    p3 = ax.barh(left, python_len_list, left=cpp_len_list +
                 others_len_list, color="lightblue")
    ax.legend((p1[0], p2[0], p3[0]), ("Others", "C++", "Python"))
    ax.set_xlabel('Score')
    ax.set_ylabel('Users')
    ax.set_yticklabels(users_list, fontdict=None, minor=False)
    canvas = FigureCanvas(fig)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)

    return response


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        users = User.objects
        results = Result.objects
        for user in users.all():
            user.score = len(results.filter(user=user)) * 100
            language_list = [
                result.result_language for result in results.filter(user=user)]
            if language_list != []:
                user.main_language = Counter(
                    language_list).most_common(1)[0][0]
            user.save()
        user_rank = users.order_by('-score')
        context['users'] = user_rank[:3]
        # context['graph'] = create_graph(users, results)
        return render(self.request, self.template_name, context)


class MyPageView(LoginRequiredMixin, TemplateView):
    template_name = 'mypage.html'

    def get(self, request, *args, **kwargs):
        context = super(MyPageView, self).get_context_data(**kwargs)
        current_user = request.user.id
        c_user = User(id=current_user)
        results = Result.objects.filter(user=c_user)
        score = len(results) * 100
        context['results'] = results
        context['c_user'] = c_user
        context['score'] = score
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
            )
            user.set_password(data['password'])
            user.save()
            print("saved")
            render(self.request, 'user_done.html', {'form': form})

        else:
            render(self.request, self.template_name, {'form': form})


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
        problems = AtCoderProblem.objects.all()
        context['problems'] = problems[::-1]
        return render(self.request, self.template_name, context)


class GetProblemsView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        context = super(GetProblemsView, self).get_context_data(**kwargs)

        '''
        関数を入れ子にしすぎて読みにくくなってる！

        get_context_dataをオーバーライドして、その中で関数使わずにスッキリ完結させて！
        スクレイプするところまで全部get_context_dataの中で書いてもいいと思うけど、それが
        嫌だったらgetの中に分けて書くとか、一つぐらいならメソッド作ってもいいかも（読みやすくなるなら）
        '''

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
        problems = AtCoderProblem.objects.all()
        existing_contest_list = [str(problems[i])
                                 for i in range(len(problems))]
        atcoder_contest_archive = get_contest_links(
            'https://atcoder.jp/contest/archive')
        contest_list = list(atcoder_contest_archive.keys())[:5]
        for contest in contest_list:
            if contest not in existing_contest_list:
                if "Regular" in contest:
                    tasks_dict = get_tasks(contest)
                    problem = AtCoderProblem(
                        problem_name=contest,
                        task_c=tasks_dict['C'],
                        task_d=tasks_dict['D'],
                        task_e=tasks_dict['E'],
                        task_f=tasks_dict['F'],
                    )
                elif "Grand" in contest:
                    tasks_dict = get_tasks(contest)
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


class CreatePostsView(LoginRequiredMixin, TemplateView):
    template_name = 'create_posts.html'
    model = Result
    form_class = CreatePostsForm
    success_url = '/ranking/posts/'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        print("posted")
        if form.is_valid():
            now = timezone.now()
            data = form.cleaned_data
            result = Result(user=request.user,
                            result_problem=data['result_problem'],
                            result_language=data['result_language'],
                            result_coding_time=data['result_coding_time'],
                            result_running_time=data['result_running_time'],
                            pub_date=now,
                            result_code=data['result_code']
                            )
            result.save()
            print("saved")
            return render(self.request, 'posts_done.html', {'form': form})

        else:
            return render(self.request, self.template_name, {'form': form})


class PostsView(LoginRequiredMixin, TemplateView):
    template_name = 'posts.html'

    def get(self, request, *args, **kwargs):
        context = super(PostsView, self).get_context_data(**kwargs)
        results = Result.objects.all()
        context['results'] = results[::-1][:100]
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
    form_class = LoginForm

    def get(self, _, *args, **kwargs):
        if self.request.user.is_authenticated():
            return redirect(self.get_next_redirect_url())
        else:
            form = self.form_class(self.request.POST)
            return render(self.request, self.template_name, {'form': form})
            # return auth_views.login(self.request, *args, **kwargs)

    def post(self, _, *args, **kwargs):
        form = self.form_class(self.request.POST)
        username = form['username']
        password = form['password']
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth_views.login(self.request, user)
            return redirect(self.get_next_redirect_url())
        else:
            kwargs = {'template_name': 'login.html'}
            return auth_views.login(self.request, *args, **kwargs)

    def get_next_redirect_url(self):
        redirect_url = self.request.GET.get('next')
        if not redirect_url or redirect_url == '/ranking/':
            redirect_url = '/ranking/'

        return redirect_url


def logout(request):
    context = {
        'template_name': 'logout.html',
    }
    return auth_views.logout(request, **context)
