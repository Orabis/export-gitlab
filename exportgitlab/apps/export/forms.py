from django import forms

from .models import *


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["gitlab_token"]


class GitlabIDForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["gitlab_id"]
