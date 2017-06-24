from django.test import TestCase, Client

from ranking.commons.libraries import *
from ranking.tests.factory import *


class ServiceTestTool(object):
    @classmethod
    def login(cls, client, user, password):
        client.post('/login',
                    {'username': user.identifier, 'password': password},
                    follow=True)
        return client

# Test ranking is showed,and graph is showed


class IndexViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory.create()
        cls.atcoderproblem = AtCoderProblemFactory.create()
        cls.result = ResultFactory.create()

    def setUp(self):
        self.user = IndexViewTest.user
        self.atcoderproblem = IndexViewTest.atcoderproblem
        self.result = IndexViewTest.result
        self.client = ServiceTestTool.login(
            Client(), IndexViewTest.user, 'ranking_password')

    def test_index_ranking(self):
        # create 10 testusers
        for i in range(10):
            user = User(
                username='test_user{0}'.format(i),
                arc_user_name='user{0}'.format(i),
                email='email{0}@email.com'.format(i),
            )
            user.set_password('password{0}'.format(i))
            user.save()
        # create posts for testusers:
        for i in range(30):
            result = Result(user=User(username='test_user1'),
                            result_problem=AtCoderProblem.objects.get(id=1),
                            result_language='Python',
                            result_coding_time=3,
                            result_running_time=4,
                            pub_date=datetime.date(2008, 10, 5),
                            result_code='sample_code'
                            )
            result.save()

        for i in range(10):
            result = Result(user=User(username='test_user2'),
                            result_problem=AtCoderProblem.objects.get(id=1),
                            result_language='Python',
                            result_coding_time=3,
                            result_running_time=4,
                            pub_date=datetime.date(2008, 10, 5),
                            result_code='sample_code'
                            )
            result.save()

        for i in range(40):
            result = Result(user=User(username='test_user3'),
                            result_problem=AtCoderProblem.objects.get(id=1),
                            result_language='Python',
                            result_coding_time=3,
                            result_running_time=4,
                            pub_date=datetime.date(2008, 10, 5),
                            result_code='sample_code'
                            )
            result.save()

        for i in range(10):
            result = Result(user=User(username='test_user4'),
                            result_problem=AtCoderProblem.objects.get(id=1),
                            result_language='Python',
                            result_coding_time=3,
                            result_running_time=4,
                            pub_date=datetime.date(2008, 10, 5),
                            result_code='sample_code'
                            )
            result.save()

        for i in range(20):
            result = Result(user=User(username='test_user5'),
                            result_problem=AtCoderProblem.objects.get(id=1),
                            result_language='Python',
                            result_coding_time=3,
                            result_running_time=4,
                            pub_date=datetime.date(2008, 10, 5),
                            result_code='sample_code'
                            )
            result.save()

        response = self.client.get('/ranking/')

        self.assertContains(response, "test_user1")
        self.assertContains(response, "test_user3")
        self.assertContains(response, "test_user5")
        self.assertNotContains(response, "test_user2")
        self.assertNotContains(response, "test_user4")


'''
# Test if user is successfully created


class UsersViewTest(TestCase):

    # Test if posts is successfully created


class PostsViewTest(TestCase):
'''
