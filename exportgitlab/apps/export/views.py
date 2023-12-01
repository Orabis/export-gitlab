from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_list_or_404
from .forms import UserForm
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from .models import *


@login_required
def profile(request):
    return render(request, "export/profile.html", {"user": request.user})


@login_required
def changetoken(request):
    user = request.user
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, _("Gitlab token modified"))
            return redirect("profile")
        else:
            messages.add_message(request, messages.ERROR, _("Wrong Gitlab token"))
    else:
        form = UserForm(instance=user)
    return render(request, "export/change_token_pending.html", {"form": form})


def projects(request):
    all_projects = get_list_or_404(Project)
    paginator = Paginator(all_projects, 10)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "export/projects_list.html", {"Project": all_projects, "page_obj": page_obj})


def index(request):
    return redirect("projects")
