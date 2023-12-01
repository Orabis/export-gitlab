from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class Project(models.Model):
    gitlab_id = models.IntegerField(null=False)
    name = models.CharField(null=False)
    description = models.CharField(default=None, null=True, blank=True)
    url = models.CharField(null=False)

    def __str__(self):
        return self.name


class User(AbstractUser):
    gitlab_token = models.CharField(
        max_length=40, blank=True, default=None, help_text=_("Gitlab personal token"), null=True)
    projects = models.ManyToManyField(Project)
