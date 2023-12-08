import markdown2
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import (
    get_list_or_404,
    get_object_or_404,
    redirect,
    render,
)
from django.utils.translation import gettext_lazy as _
from gitlab import GitlabGetError
from gitlab.v4.objects import Project as GLProject

from exportgitlab.libs.connect import gl_connection

from .forms import *
from .models import *


class NoTokenError(Exception):
    pass


def get_token_or_redirect(request):
    useractualtoken = request.user.gitlab_token
    if not useractualtoken:
        messages.add_message(request, messages.WARNING, _("No Gitlab token found"))
        raise NoTokenError(f"user {request.user.username} has no gitlabtoken")
    return useractualtoken


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


@login_required
def projects(request):
    all_projects = get_list_or_404(Project)
    paginator = Paginator(all_projects, 10)
    try:
        useractualtoken = get_token_or_redirect(request)
        gl = gl_connection(useractualtoken)
    except NoTokenError:
        return redirect("profile")

    if request.method == "POST":
        form = GitlabIDForm(request.POST)
        if form.is_valid():
            project_id = form.cleaned_data["gitlab_id"]
            try:
                project: GLProject = gl.projects.get(project_id)
                projectmodel: Project = form.save(commit=False)
                projectmodel.url = project.web_url
                projectmodel.name = project.name_with_namespace
                projectmodel.description = project.description
                projectmodel.save()
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    _("Project : [%(project_name)s] added to database. id : %(project_id)s")
                    % {"project_name": project.name_with_namespace, "project_id": project_id},
                )
                return redirect("projects")

            except GitlabGetError as e:
                if e.response_code == 404:
                    messages.add_message(request, messages.ERROR, _("Project does not exist"))
                else:
                    messages.add_message(request, messages.ERROR, _("An error occurred while checking the project"))
        else:
            messages.add_message(request, messages.ERROR, _("GitID invalid (Error in entering the ID)"))
    else:
        form = GitlabIDForm()

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "export/projects_list.html", {"page_obj": page_obj, "form": form})


def refresh(request, id_pj):
    try:
        useractualtoken = get_token_or_redirect(request)
        gl = gl_connection(useractualtoken)
    except NoTokenError:
        return redirect("profile")

    the_project = Project.objects.get(id=id_pj)
    project_info = gl.projects.get(the_project.gitlab_id)
    Project.name = project_info.name_with_namespace
    Project.description = project_info.description
    Project.url = project_info.web_url
    Project.objects.update()
    messages.add_message(
        request,
        messages.SUCCESS,
        _("Refresh of [%(project_name)s] complete. id : %(project_id)d")
        % {"project_name": project_info.name_with_namespace, "project_id": the_project.gitlab_id},
    )

    return redirect("projects")


@login_required
def issues(request, id_pj):
    the_project: Project = get_object_or_404(Project, id=id_pj)

    try:
        useractualtoken = get_token_or_redirect(request)
        gl = gl_connection(useractualtoken)
    except NoTokenError:
        return redirect("profile")
    gitlab_project: GLProject = gl.projects.get(the_project.gitlab_id)
    list_issues = gitlab_project.issues.list(get_all=True, state="opened")
    gitlab_labels = gitlab_project.labels.list()
    gitlab_labels_dict = {}
    for label in gitlab_labels:
        gitlab_labels_dict[label.name] = label.color

    paginator = Paginator(list_issues, 100)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "export/issues_list.html",
        {"the_project": the_project, "page_obj": page_obj, "gitlab_labels": gitlab_labels_dict},
    )


@login_required
def download(request, id_pj):
    the_project: Project = get_object_or_404(Project, id=id_pj)
    try:
        useractualtoken = get_token_or_redirect(request)
        gl = gl_connection(useractualtoken)
    except NoTokenError:
        return redirect("profile")
    gitlab_project: GLProject = gl.projects.get(the_project.gitlab_id)

    if request.method == "POST":
        issues_list = request.POST.getlist("checkbox_issues")
        issues_data = []
        for issue_id in issues_list:
            list_issues = gitlab_project.issues.get(issue_id)
            html_title = markdown2.markdown(list_issues.title)
            html_description = markdown2.markdown(list_issues.description)
            issues_data.append(
                {
                    "id": issue_id,
                    "title": html_title,
                    "description": html_description,
                }
            )
        return render(request, "export/output.html", {"issues_data": issues_data})

    return redirect("projects")


def index(request):
    return redirect("projects")
