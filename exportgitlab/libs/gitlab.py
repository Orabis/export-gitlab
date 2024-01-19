import gitlab

from exportgitlab.libs.color_contrast import passes


def gl_connection(user_token):
    gl = gitlab.Gitlab(url="https://git.unistra.fr", private_token=user_token)
    gl.auth()
    return gl


def get_labels_list(gitlab_project):
    gitlab_labels = gitlab_project.labels.list(get_all=True)
    gitlab_labels_dict = []
    for label in gitlab_labels:
        accessibility_color_check = passes(label.color, "#ffffff")
        if accessibility_color_check:
            gitlab_labels_dict.append(
                {"name": label.name, "bg_color": label.color, "text_color": "#FFFFF", "id": label.id}
            )
        else:
            gitlab_labels_dict.append(
                {"name": label.name, "bg_color": label.color, "text_color": "#000000", "id": label.id}
            )
    return gitlab_labels_dict


def get_issues(gitlab_project):
    issues_data = []
    gitlab_issues = gitlab_project.issues.list(get_all=True)
    for gitlab_issue in gitlab_issues:
        issues_data.append(
            {
                "iid": gitlab_issue.iid,
                "title": gitlab_issue.title,
                "states": gitlab_issue.state,
                "labels": gitlab_issue.labels,
                "author": gitlab_issue.author["name"],
            }
        )
    return issues_data
