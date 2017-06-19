from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class User(AbstractBaseUser):
    username = models.CharField(max_length=15)
    arc_user_name = models.CharField(max_length=15, default='')
    email = models.EmailField(
        verbose_name='email address', max_length=185, blank=False, unique=True, default='')
    is_validated = models.BooleanField(default=False)
    # answered_problem = models.ManyToManyField(AtCoderProblem, blank=True)
    USERNAME_FIELD = 'identifier'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


class AtCoderProblem(models.Model):
    user = models.ManyToManyField(User)
    problem_name = models.CharField(max_length=20)
    task_a = models.CharField(max_length=500, blank=True, null=True)
    task_b = models.CharField(max_length=500, blank=True, null=True)
    task_c = models.CharField(max_length=500, blank=True, null=True)
    task_d = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.problem_name


class AGCProblem(AtCoderProblem):
    task_e = models.CharField(max_length=500, blank=True, null=True)
    task_f = models.CharField(max_length=500, blank=True, null=True)


class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    result_problem = models.ForeignKey(
        AtCoderProblem, on_delete=models.CASCADE)
    result_language = models.CharField(max_length=15)
    result_coding_time = models.IntegerField(default=0)
    result_running_time = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published')
    result_code = models.CharField(max_length=500, blank=True, null=True)

    def __int__(self):
        return self.id
