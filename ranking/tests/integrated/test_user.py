from django.test import TestCase, Client

from atcoder_ranking.commons.libraries import *
from ranking.tests.factory import *


class ServiceTestTool(object):
    @classmethod
    def login(cls, client, user, password):
        client.post('/ranking/login/',
                    {'username': user.username, 'password': password},
                    follow=True)
        return client

# Test ranking is showed
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
        self.client = ServiceTestTool.login(Client(), IndexViewTest.user, 'ranking_password')

    def test_index_ranking(self):
        # create 10 testusers
        users = [UserFactory.create() for i in range(10)]
        # create posts for testusers:
        result1 = [ResultFactory.create(user=users[1]) for i in range(30)]
        result2 = [ResultFactory.create(user=users[2]) for i in range(20)]
        result3 = [ResultFactory.create(user=users[3]) for i in range(40)]
        result4 = [ResultFactory.create(user=users[4]) for i in range(10)]
        result5 = [ResultFactory.create(user=users[5]) for i in range(5)]
        result6 = [ResultFactory.create(user=users[6]) for i in range(50)]

        response = self.client.get('/ranking/')

        self.assertContains(response, users[1].username)
        self.assertContains(response, users[3].username)
        self.assertContains(response, users[6].username)
        self.assertNotContains(response, users[2].username)
        self.assertNotContains(response, users[4].username)
        self.assertNotContains(response, users[5].username)
        self.assertNotContains(response, users[0].username)


class MyPageViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory.create()
        cls.atcoderproblem = AtCoderProblemFactory.create()
        cls.result = ResultFactory.create()

    def setUp(self):
        self.user = MyPageViewTest.user
        self.atcoderproblem = MyPageViewTest.atcoderproblem
        self.result = MyPageViewTest.result
        self.client = ServiceTestTool.login(Client(), MyPageViewTest.user, 'ranking_password')

    def test_posts_create(self):
        # create 10 testusers
        users = [UserFactory.create() for i in range(10)]
        # create posts for testusers:
        result1 = [ResultFactory.create(user=users[1]) for i in range(30)]
        result2 = [ResultFactory.create(user=users[2]) for i in range(20)]
        result3 = [ResultFactory.create(user=users[3]) for i in range(40)]
        result4 = [ResultFactory.create(user=users[4]) for i in range(10)]
        result5 = [ResultFactory.create(user=users[5]) for i in range(5)]
        result6 = [ResultFactory.create(user=users[6]) for i in range(50)]
        result_self=[ResultFactory.create(user=self.user) for i in range(10)]

        response = self.client.get('/ranking/mypage/')

        self.assertContains(response, self.user.username)
        self.assertContains(response, 100)
        self.assertContains(response, 'Python')

class PostsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory.create()
        cls.atcoderproblem = AtCoderProblemFactory.create()
        cls.result = ResultFactory.create()

    def setUp(self):
        self.user = PostsViewTest.user
        self.atcoderproblem = PostsViewTest.atcoderproblem
        self.result = PostsViewTest.result
        self.client = ServiceTestTool.login(Client(), PostsViewTest.user, 'ranking_password')

    def test_posts_create(self):
        # create 10 testusers
        users = [UserFactory.create() for i in range(10)]
        # create posts for testusers:
        result1 = [ResultFactory.create(user=users[1]) for i in range(30)]
        result2 = [ResultFactory.create(user=users[2]) for i in range(20)]
        result3 = [ResultFactory.create(user=users[3]) for i in range(40)]
        result4 = [ResultFactory.create(user=users[4]) for i in range(10)]
        result5 = [ResultFactory.create(user=users[5]) for i in range(5)]
        result6 = [ResultFactory.create(user=users[6]) for i in range(50)]

        response = self.client.get('/ranking/posts/')

        self.assertContains(response, 'AtCoder')
        self.assertContains(response, 'Python')

        self.assertContains(response, users[1].username)
        self.assertContains(response, users[2].username)
        self.assertContains(response, users[3].username)
        self.assertContains(response, users[4].username)
        self.assertContains(response, users[5].username)
        self.assertContains(response, users[6].username)
        self.assertNotContains(response, users[0].username)
        self.assertNotContains(response, users[7].username)
