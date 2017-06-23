from django.test import TestCase

# Create your tests here.


class CreateUserViewTest(TestCase):
    def setUp(self):
        test_user = User.objects.create(username='name',
                                        email='a@a.com',
                                        arc_user_name='coder',
                                        password='nonenone')

    def test_user_can_login(self):
        self.assertIs(user.is_vaild(), True)

    def test_user_is_created(self):
        user = User.objects.create(uesrname='name')
        self.assetIs()
