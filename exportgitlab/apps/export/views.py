from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from gitlab import GitlabGetError
from gitlab.v4.objects import Project as GLProject

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
    project_models = Project.objects.all()
    paginator = Paginator(project_models, 10)

    if request.GET.get("project_name_filter"):
        name_filter = request.GET.get("project_name_filter")
        all_projects = Project.objects.filter(name__contains=name_filter)
        paginator = Paginator(all_projects, 10)

    if request.method == "POST":
        form = GitlabIDForm(request.POST)
        if form.is_valid():
            project_id = form.cleaned_data["gitlab_id"]
            try:
                project_gitlab: GLProject = request.gl.projects.get(project_id)
                project_model: Project = form.save(commit=False)
                project_model.url = project_gitlab.web_url
                project_model.name = project_gitlab.name_with_namespace
                project_model.description = project_gitlab.description
                project_model.save()
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    _("Project : [%(project_name)s] added to database. id : %(project_id)s")
                    % {"project_name": project_model.name, "project_id": project_id},
                )
                return redirect("list_all_projects_homepage")

            except GitlabGetError as e:
                if e.response_code == 404:
                    messages.add_message(request, messages.ERROR, _("Project does not exist"))
                else:
                    messages.add_message(request, messages.ERROR, _("An error occurred while checking the project"))
        else:
            messages.add_message(
                request,
                messages.ERROR,
                _("ID error (Project is already in the database ? Error in entering the ID ?)"),
            )
    else:
        form = GitlabIDForm()

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "export/projects_list.html", {"page_obj": page_obj, "form": form})


@login_required
@gitlab_valid_auth_required
def refresh_project(request, id_pj):
    try:
        project_model = Project.objects.get(id=id_pj)
        project_info = request.gl.projects.get(project_model.gitlab_id)
        project_model.name = project_info.name_with_namespace
        project_model.description = project_info.description
        project_model.url = project_info.web_url
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
    gitlab_project: GLProject = request.gl.projects.get(project_model.gitlab_id)
    gitlab_labels_dict = get_labels_list(gitlab_project)
    iid_filter = [request.GET.get("iid")]
    labels_filter = request.GET.getlist("lab")
    opened_closed_filter = request.GET.get("oc")

    list_issues = get_issues(gitlab_project, iid_filter, labels_filter, opened_closed_filter)
    paginator = Paginator(list_issues, 25)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "export/issues_list.html",
        {"project": project_model, "page_obj": page_obj, "gitlab_labels": gitlab_labels_dict},
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


def index(request):
    return redirect("list_all_projects_homepage")
