from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, identifier, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        customer = self.model(identifier=identifier,
                              email=self.normalize_email(email))
        customer.set_password(password)
        customer.save(using=self._db)
        return customer


class User(AbstractBaseUser):
    object = UserManager()
    identifier = models.CharField(max_length=15)
    arc_user_name = models.CharField(max_length=15, default='')
    email = models.EmailField(
        verbose_name='email address', max_length=185, blank=False, unique=True, default='')
    is_validated = models.BooleanField(default=False)
    USERNAME_FIELD = 'identifier'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.user_name


class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    result_question = models.IntegerField(default=0)
    result_coding_time = models.IntegerField(default=0)
    result_running_time = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published')
    result_code = models.CharField(max_length=500)

    def __str__(self):
        return self.result_code
