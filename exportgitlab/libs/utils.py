import base64
import datetime
import json

import markdown2
import requests
from bs4 import BeautifulSoup
from django.conf import settings
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from gitlab import GitlabAuthenticationError


def convert_html(text, default_value="<p>Aucune description</p>"):
    if text is None:
        return default_value
    return markdown2.markdown(text, extras=["tables"])


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


def get_token_or_redirect(request):
    user_token = request.user.gitlab_token
    if not user_token:
        raise GitlabAuthenticationError(
            _("user %(username)s has no GitLab Token") % {"username": request.user.username}
        )
    return user_token

def find_img_and_convert(soup, gitlab_project):
    project_id = gitlab_project.id 
    for img_link in soup.find_all("img"):
        img_src = img_link["src"]
        if img_src.startswith("/-/"):
            full_url = f"{gitlab_project.web_url}{img_src}"
        else:
            full_url = f"https://gitlab.com/-/project/{project_id}{img_src}"
        r = requests.get(full_url)
        if r.status_code == 200:
            image_encode = base64.b64encode(r.content).decode("utf-8")
            type_mime = r.headers["Content-Type"]
            img_link["src"] = f"data:{type_mime};base64,{image_encode}"
        else:
            print(f"Échec du téléchargement de {full_url}")
    return str(soup)

def html_make_data(issue_id, gitlab_project):
    list_issues = gitlab_project.issues.get(issue_id)
    html_title = list_issues.title
    html_description = convert_html(list_issues.description)
    soup = BeautifulSoup(html_description, "html.parser")
    html_description = find_img_and_convert(soup, gitlab_project)
    return html_title, html_description


class PDFGenerationError(Exception):
    pass
