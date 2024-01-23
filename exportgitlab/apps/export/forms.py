from django import forms
from django.forms import PasswordInput

from .models import *


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["gitlab_token"]
        widgets = {
            "gitlab_token": PasswordInput(render_value=True),
        }
