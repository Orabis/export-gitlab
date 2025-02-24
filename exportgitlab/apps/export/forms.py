from django import forms
from django.forms import PasswordInput
from django.utils.translation import gettext_lazy as _
from .models import *


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["gitlab_token"]
        widgets = {
            "gitlab_token": PasswordInput(render_value=True),
        }

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label=_("Username")
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        label=_("Password")
    )

class RegisterForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "ex: john doe"}),
        label=_("Username")
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "ex: contact@domain.com"}),
        label=_("Email")
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": _("8 characters required with at least one letter and one number")}),
        label=_("Password")
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": _("confirm the password")}),
        label=_("Confirm password")
    )
    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Les mots de passe ne correspondent pas.")

        return cleaned_data