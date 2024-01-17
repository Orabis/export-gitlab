import zipfile
from io import BytesIO

from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from exportgitlab.libs.utils import *


def issues_report_generate_ungroup(request, issues_list, gitlab_project, id_pj):
    if len(issues_list) != 0:
        zipped_content = BytesIO()
        with zipfile.ZipFile(zipped_content, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
            for issue_id in issues_list:
                html_title, html_description = html_make_data(issue_id, gitlab_project)
                issues_data = [{"id": issue_id, "title": html_title, "description": html_description}]
                html = render_to_string("export/html_to_pdf_output.html", {"issues_data": issues_data}, request)
                try:
                    data = html_to_pdf(html)
                except PDFGenerationError as e:
                    messages.add_message(request, messages.ERROR, _("ErrorPDF"))
                    raise PDFGenerationError("PDF generation error")

                try:
                    zf.writestr(f"issue_{issue_id}.pdf", data)
                except FileExistsError:
                    pass
            zf.close()
            response = HttpResponse(zipped_content.getvalue(), content_type="application/zip")
            response["Content-Disposition"] = f'attachement; filename="multiple_issues.zip"'
            return response
    else:
        messages.add_message(request, messages.ERROR, _("No issues checked"))
        return redirect("list_all_issues", id_pj)


def issues_report_generate_group(request, issues_list, gitlab_project, id_pj):
    if len(issues_list) != 0:
        issues_data = []
        for issue_id in issues_list:
            html_title, html_description = html_make_data(issue_id, gitlab_project)
            issues_data.append({"id": issue_id, "title": html_title, "description": html_description})
        html = render_to_string("export/html_to_pdf_output.html", {"issues_data": issues_data}, request)
        try:
            data = html_to_pdf(html)
        except PDFGenerationError as e:
            messages.add_message(request, messages.ERROR, _("ErrorPDF"))
            raise PDFGenerationError("PDF generation error")
        response = HttpResponse(data, content_type="application/pdf")
        if len(issues_list) >= 2:
            response[
                "Content-Disposition"
            ] = f'attachement; filename="issues {issues_list[0]} - {issues_list[-1]}.pdf"'
        else:
            response["Content-Disposition"] = f'attachement; filename="issue {issues_list[0]}.pdf"'
        return response
    else:
        messages.add_message(request, messages.ERROR, _("No issues checked"))
        return redirect("list_all_issues", id_pj)
