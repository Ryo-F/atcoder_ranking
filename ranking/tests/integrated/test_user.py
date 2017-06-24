from django.test import TestCase, Client

from atcoder_ranking.commons.libraries import *
from ranking.tests.factory import *


class ServiceTestTool(object):
    @classmethod
    def login(cls, client, user, password):
<<<<<<< HEAD
        client.post('/ranking/login/',
=======
        client.post('/login',
>>>>>>> 0c512f327f98e71dd20af618735ccbbf7d716b61
                    {'username': user.username, 'password': password},
                    follow=True)
        return client

<<<<<<< HEAD
# Test ranking is showed
=======
# Test ranking is showed,and graph is showed


>>>>>>> 0c512f327f98e71dd20af618735ccbbf7d716b61
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
<<<<<<< HEAD
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
=======
        self.client = ServiceTestTool.login(
            Client(), IndexViewTest.user, 'ranking_password')

    def test_index_ranking(self):
        # create 10 testusers
        for i in range(10):
            user = User(
                username='testing_user{0}'.format(i),
                arc_user_name='user{0}'.format(i),
                email='email{0}@email.com'.format(i),
            )
            user.set_password('password{0}'.format(i))
            user.save()
        # create posts for testusers:
        for i in range(30):
            result = Result(user=User(username='testing_user1'),
                            result_problem=AtCoderProblem.objects.get(id=1),
                            result_language='Python',
                            result_coding_time=3,
                            result_running_time=4,
                            pub_date=datetime.date(2008, 10, 5),
                            result_code='sample_code'
                            )
            result.save()

        for i in range(10):
            result = Result(user=User(username='testing_user2'),
                            result_problem=AtCoderProblem.objects.get(id=1),
                            result_language='Python',
                            result_coding_time=3,
                            result_running_time=4,
                            pub_date=datetime.date(2008, 10, 5),
                            result_code='sample_code'
                            )
            result.save()

        for i in range(40):
            result = Result(user=User(username='testing_user3'),
                            result_problem=AtCoderProblem.objects.get(id=1),
                            result_language='Python',
                            result_coding_time=3,
                            result_running_time=4,
                            pub_date=datetime.date(2008, 10, 5),
                            result_code='sample_code'
                            )
            result.save()

        for i in range(10):
            result = Result(user=User(username='testing_user4'),
                            result_problem=AtCoderProblem.objects.get(id=1),
                            result_language='Python',
                            result_coding_time=3,
                            result_running_time=4,
                            pub_date=datetime.date(2008, 10, 5),
                            result_code='sample_code'
                            )
            result.save()

        for i in range(20):
            result = Result(user=User(username='testing_user5'),
                            result_problem=AtCoderProblem.objects.get(id=1),
                            result_language='Python',
                            result_coding_time=3,
                            result_running_time=4,
                            pub_date=datetime.date(2008, 10, 5),
                            result_code='sample_code'
                            )
            result.save()

        response = self.client.get('/ranking/')

        self.assertContains(response, "testing_user1")
        self.assertContains(response, "testing_user3")
        self.assertContains(response, "testing_user5")
        self.assertNotContains(response, "testing_user2")
        self.assertNotContains(response, "testing_user4")


'''
# Test if user is successfully created


class UsersViewTest(TestCase):

    # Test if posts is successfully created


class PostsViewTest(TestCase):
'''
>>>>>>> 0c512f327f98e71dd20af618735ccbbf7d716b61
