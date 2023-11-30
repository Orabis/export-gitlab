from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserForm
from django.contrib import messages


@login_required
def profile(request):
    return render(request, "profile.html", {"user": request.user})


@login_required
def changetoken(request):
    user = request.user
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, "Le token GitLab a bien été modifié")
            return redirect("profile")
        else:
            messages.add_message(request, messages.ERROR, "Le token GitLab est erroné")
    else:
        form = UserForm(instance=user)
    return render(request, "change_token_pending.html", {"form": form})
