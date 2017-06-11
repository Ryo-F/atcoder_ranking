from django.contrib import admin

# Register your models here.
from .models import User, Result

admin.site.register([Result, User])
