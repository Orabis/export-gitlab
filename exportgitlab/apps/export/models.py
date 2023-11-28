from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.

class User(AbstractUser):
    gitlab_token = models.CharField(max_length=40, default='null', help_text=_('Gitlab personal token'))
