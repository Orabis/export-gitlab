import base64
import datetime
import json

import markdown2
import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, QueryDict
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from gitlab import GitlabGetError
from gitlab.v4.objects import Project as GLProject

from exportgitlab.libs.connect import gl_connection

from .forms import *
from .models import *


class NoTokenError(Exception):
    pass


class PDFGenerationError(Exception):
    pass


def get_token_or_redirect(request):
    user_token = request.user.gitlab_token
    if not user_token:
        messages.add_message(request, messages.WARNING, _("No Gitlab token found"))
        raise NoTokenError(f"user {request.user.username} has no gitlabtoken")
    return user_token


def html_to_pdf(html: str) -> bytes:
    url: str = settings.WKHTML_TO_PDF_URL
    content: dict[str, str] = {
        "contents": base64.b64encode(html.encode("utf-8")).decode("utf-8"),
        "options": {
            "footer-font-size": "4",
            "footer-right": "[page] / [topage]",
            "footer-left": datetime.date.today().strftime("%d %m %Y"),
        },
    }
    headers: dict[str, str] = {
        "Content-Type": "application/json",
    }
    response: requests.Response = requests.post(url, data=json.dumps(content), headers=headers)

    if not response.ok:
        raise PDFGenerationError(response.content)

    return response.content


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
def list_all_projects_homepage(request):
    all_projects = Project.objects.all()
    paginator = Paginator(all_projects, 10)
    try:
        user_token = get_token_or_redirect(request)
        gl = gl_connection(user_token)
    except NoTokenError:
        return redirect("user_profile")

    if request.method == "POST":
        form = GitlabIDForm(request.POST)
        if form.is_valid():
            project_id = form.cleaned_data["gitlab_id"]
            try:
                project: GLProject = gl.projects.get(project_id)
                project_model: Project = form.save(commit=False)
                project_model.url = project.web_url
                project_model.name = project.name_with_namespace
                project_model.description = project.description
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
            messages.add_message(request, messages.ERROR, _("GitID invalid (Error in entering the ID)"))
    else:
        form = GitlabIDForm()

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "export/projects_list.html", {"page_obj": page_obj, "form": form})


def refresh_project(request, id_pj):
    try:
        user_token = get_token_or_redirect(request)
        gl = gl_connection(user_token)
    except NoTokenError:
        return redirect("user_profile")

    project_model = Project.objects.get(id=id_pj)
    project_info = gl.projects.get(project_model.gitlab_id)
    Project.name = project_info.name_with_namespace
    Project.description = project_info.description
    Project.url = project_info.web_url
    Project.objects.update()
    messages.add_message(
        request,
        messages.SUCCESS,
        _("Refresh of [%(project_name)s] complete. id : %(project_model_gitlab_id)d")
        % {"project_name": Project.name, "project_model_gitlab_id": project_model.gitlab_id},
    )

    return redirect("list_all_projects_homepage")


@login_required
def list_all_issues(request, id_pj):
    project: Project = get_object_or_404(Project, id=id_pj)

    try:
        user_token = get_token_or_redirect(request)
        gl = gl_connection(user_token)
    except NoTokenError:
        return redirect("user_profile")

    project_model: GLProject = gl.projects.get(project.gitlab_id)
    gitlab_labels = project_model.labels.list()
    gitlab_labels_dict = {label.name: label.color for label in gitlab_labels}

    if QueryDict(request.GET.urlencode()):
        iid_filter = [request.GET.get("iid")]
        labels_filter = [request.GET.get("lab")]
        opened_closed_filter = request.GET.get("oc")
        if iid_filter[0] == "":
            iid_filter = None
        if labels_filter == [None]:
            list_issues = project_model.issues.list(state=opened_closed_filter, iids=iid_filter)
        else:
            list_issues = project_model.issues.list(state=opened_closed_filter, iids=iid_filter, labels=labels_filter)
    else:
        list_issues = project_model.issues.list(get_all=True, state="opened")

    paginator = Paginator(list_issues, 100)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "export/issues_list.html",
        {"project": project, "page_obj": page_obj, "gitlab_labels": gitlab_labels_dict},
    )


@login_required
def download_report_issues(request, id_pj):
    project: Project = get_object_or_404(Project, id=id_pj)
    try:
        user_token = get_token_or_redirect(request)
        gl = gl_connection(user_token)
    except NoTokenError:
        return redirect("user_profile")
    project_model: GLProject = gl.projects.get(project.gitlab_id)

    if request.method == "POST":
        issues_list = request.POST.getlist("checkbox_issues")
        issues_data = []
        for issue_id in issues_list:
            list_issues = project_model.issues.get(issue_id)
            html_title = markdown2.markdown(list_issues.title)
            html_description = markdown2.markdown(list_issues.description)
            issues_data.append(
                {
                    "id": issue_id,
                    "title": html_title,
                    "description": html_description,
                }
            )
        html = render_to_string("export/html_to_pdf_output.html", {"issues_data": issues_data}, request)
        try:
            data = html_to_pdf(html)
        except PDFGenerationError as e:
            messages.add_message(request, messages.ERROR, _("ErrorPDF"))
            raise PDFGenerationError("PDF generation error")
        response = HttpResponse(data, content_type="application/pdf")
        response["Content-Disposition"] = f'attachement; filename="issue {issues_list}.pdf"'
        return response
    messages.add_message(request, messages.ERROR, _("Error downloading issues"))
    return redirect("list_all_projects_homepage")


def index(request):
    return redirect("list_all_projects_homepage")
