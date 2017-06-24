from atcoder_ranking.commons.libraries import *
from django.test import TestCase, Client

from ranking.models import *


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
<<<<<<< HEAD
    username = factory.Sequence(lambda n: 'testing_user{}'.format(n))
    arc_user_name = factory.Faker('name')
    email = factory.Sequence(lambda n: 'testuser{}@gmail.com'.format(n))
    password = factory.PostGenerationMethodCall(
        'set_password', 'ranking_password')
=======
    username = factory.Faker('name')
    arc_user_name = factory.Faker('name')
    email = factory.Sequence(lambda n: 'testuser{}@gmail.com'.format(n))
    password = factory.PostGenerationMethodCall(
        'set_password', 'scouty_password')
>>>>>>> 0c512f327f98e71dd20af618735ccbbf7d716b61


class AtCoderProblemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AtCoderProblem
    problem_name = factory.Sequence(
        lambda n: 'AtCoder Beginner Contest {}'.format(n))
    task_a = 'task_a'
    task_b = 'task_b'
    task_c = 'task_c'
    task_d = 'task_d'


class ResultFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Result
    user = factory.SubFactory(UserFactory)
    result_problem = factory.SubFactory(AtCoderProblemFactory)
    result_language = 'Python'
    result_coding_time = 10
    result_running_time = 3
    pub_date = datetime.date(2008, 10, 5)
    result_code = 'sample_code'
