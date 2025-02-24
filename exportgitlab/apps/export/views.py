from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from gitlab import GitlabGetError
from gitlab.v4.objects import Project as GLProject
from .forms import LoginForm, RegisterForm

from ...libs.gitlab import get_issues, get_labels_list
from ...libs.reports_generation import *
from .decorators import gitlab_valid_auth_required
from .forms import *
from .models import *

@login_required
def user_profile(request):
    return render(request, "export/user_profile.html", {"user": request.user})


@login_required
def user_change_token(request):
    user = request.user
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, _("Gitlab token modified"))
            return redirect("user_profile")
        else:
            messages.add_message(request, messages.ERROR, _("Wrong Gitlab token"))
    else:
        form = UserForm(instance=user)
    return render(request, "export/change_user_token.html", {"form": form})


@login_required
@gitlab_valid_auth_required
def list_all_projects_homepage(request):
    project_models = Project.objects.filter(user=request.user)

    if request.GET.get("project_name_filter"):
        name_filter = request.GET.get("project_name_filter")
        project_models = project_models.filter(name__icontains=name_filter)

    if request.POST.get("retrieve_project"):
        gitlab_id = request.POST.get("retrieve_project")
        try:
            int(gitlab_id)
        except ValueError:
            messages.add_message(
                request,
                messages.ERROR,
                _("ID error, Invalid ID entered."),
            )
            return redirect("list_all_projects_homepage")

        try:
            project_model = Project.objects.get(gitlab_id=gitlab_id)
            request.user.projects.add(project_model)

        except Project.DoesNotExist:
            try:
                project_gitlab = request.gl.projects.get(gitlab_id)
                project_model = Project(
                    gitlab_id=project_gitlab.id,
                    name=project_gitlab.name_with_namespace,
                    url=project_gitlab.web_url,
                    description=project_gitlab.description,
                )
                project_model.save()
                request.user.projects.add(project_model)
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    _("Project : [%(project_name)s] added to database. id : %(project_id)s")
                    % {"project_name": project_model.name, "project_id": gitlab_id},
                )
                return redirect("list_all_projects_homepage")

            except GitlabGetError as e:
                if e.response_code == 404:
                    messages.add_message(request, messages.ERROR, _("Project does not exist"))
                else:
                    messages.add_message(request, messages.ERROR, _("An error occurred while checking the project"))

    paginator = Paginator(project_models, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "export/projects_list.html", {"page_obj": page_obj})


@login_required
@gitlab_valid_auth_required
def refresh_project(request, id_pj):
    try:
        project_model = Project.objects.get(id=id_pj)
        project_gitlab = request.gl.projects.get(project_model.gitlab_id)
        project_model.name = project_gitlab.name_with_namespace
        project_model.description = project_gitlab.description
        project_model.url = project_gitlab.web_url
        project_model.save()
        messages.add_message(
            request,
            messages.SUCCESS,
            _("Refresh of [%(project_name)s] complete. id : %(project_model_gitlab_id)d")
            % {"project_name": project_model.name, "project_model_gitlab_id": project_model.gitlab_id},
        )
    except GitlabGetError as e:
        if e.response_code == 404:
            messages.add_message(request, messages.ERROR, _("Project does not exist"))
        else:
            messages.add_message(request, messages.ERROR, _("An error occurred while checking the project"))

    return redirect("list_all_projects_homepage")


@login_required
@gitlab_valid_auth_required
def list_all_issues(request, id_pj):
    project_model: Project = get_object_or_404(Project, id=id_pj)
    return render(
        request,
        "export/issues_list.html",
        {"project": project_model},
    )


@login_required
@gitlab_valid_auth_required
def download_report_issues(request, id_pj):
    project_model: Project = get_object_or_404(Project, id=id_pj)
    gitlab_project: GLProject = request.gl.projects.get(project_model.gitlab_id)
    issues_list = request.POST.getlist("checkbox_issues")
    try:
        if request.method == "POST" and "ungroup_issue" in request.POST.get("grp-ungrp"):
            return issues_report_generate_ungroup(request, issues_list, gitlab_project, id_pj)

        if request.method == "POST" and "group_issue" in request.POST.get("grp-ungrp"):
            return issues_report_generate_group(request, issues_list, gitlab_project, id_pj)
    except TypeError:
        pass
    messages.add_message(request, messages.ERROR, _("Error downloading issues"))
    return redirect(reverse("list_all_issues", kwargs={"id_pj": id_pj}))


@gitlab_valid_auth_required
def project_info(request, id_pj):
    project_model: Project = get_object_or_404(Project, id=id_pj)
    gitlab_project: GLProject = request.gl.projects.get(project_model.gitlab_id)
    project_data = {"id": gitlab_project.id, "name": gitlab_project.name}
    return JsonResponse(project_data)


@gitlab_valid_auth_required
def labels_info(request, id_pj):
    project_model: Project = get_object_or_404(Project, id=id_pj)
    gitlab_project: GLProject = request.gl.projects.get(project_model.gitlab_id)
    gitlab_labels = get_labels_list(gitlab_project)
    return JsonResponse(gitlab_labels, safe=False)


@gitlab_valid_auth_required
def issues_info(request, id_pj):
    project_model: Project = get_object_or_404(Project, id=id_pj)
    gitlab_project: GLProject = request.gl.projects.get(project_model.gitlab_id)
    issues_data = get_issues(gitlab_project)
    return JsonResponse(issues_data, safe=False)


def index(request):
    return redirect("list_all_projects_homepage")

def login_view(request):
    login_form = LoginForm()
    register_form = RegisterForm()
    next_url = request.GET.get("next","home")

    if request.method == "POST":
        if "login_submit" in request.POST:
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data["username"]
                password = login_form.cleaned_data["password"]
                user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(next_url)
            else:
                login_form.add_error(None, "Identifiants incorrects")
        elif "register_submit" in request.POST:
            register_form = RegisterForm(request.POST)
            if register_form.is_valid():
                username = register_form.cleaned_data["username"]
                email = register_form.cleaned_data["email"]
                password = register_form.cleaned_data["password"]
            if User.objects.filter(username=username).exists():
                register_form.add_error("username", "Nom d'utilisateur déjà utilisé")
            elif User.objects.filter(email=email).exists():
                register_form.add_error("email", "Adresse email déjà utilisée")
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                login(request, user)
                return redirect(next_url)
    return render(request, "export/user_login.html", {"login_form": login_form, "register_form": register_form})

def logout_view(request):
    logout(request)
    return redirect("login")