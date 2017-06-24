from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, _user_has_perm)
from django.core import validators
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, username, email, password, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError('Users must have an email address.')
        email = UserManager.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            is_active=True,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        user = self.create_user(username, email, password)
        user.is_active = True
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(_('username'),max_length=30,unique=True,)
    arc_user_name = models.CharField(_('arc name'), max_length=15, blank=True)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    delete = models.BooleanField(default=0)
    score = models.IntegerField(default=0)
    main_language = models.CharField(max_length=15, default='')
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])

    def user_has_perm(user, perm, obj):
        return _user_has_perm(user, perm, obj)

    def has_perm(self, perm, obj=None):
        return _user_has_perm(self, perm, obj=obj)

    def has_module_perms(self, app_label):
        return self.is_admin

    def get_short_name(self):
        "Returns the short name for the user."
        return self.arc_user_name

    def __str__(self):
        return self.username


class AtCoderProblem(models.Model):

    users = models.ManyToManyField('User')
    problem_name = models.CharField(max_length=20)
    task_a = models.CharField(max_length=500, default='-', blank=True, null=True)
    task_b = models.CharField(max_length=500, default='-', blank=True, null=True)
    task_c = models.CharField(max_length=500, default='-', blank=True, null=True)
    task_d = models.CharField(max_length=500, default='-', blank=True, null=True)
    task_e = models.CharField(max_length=500, default='-', blank=True, null=True)
    task_f = models.CharField(max_length=500, default='-', blank=True, null=True)

    def __str__(self):
        return self.problem_name


class Result(models.Model):
    LANGUAGE_CHOICES = (
        ('Python', 'Python'),
        ('C++', 'C++'),
        ('Others', 'Others')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    result_problem = models.ForeignKey(
        AtCoderProblem, on_delete=models.CASCADE)
    result_language = models.CharField(max_length=15, choices=LANGUAGE_CHOICES)
    result_coding_time = models.IntegerField(default=0)
    result_running_time = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published')
    result_code = models.CharField(max_length=500, blank=True, null=True)

    def __int__(self):
        return self.id
