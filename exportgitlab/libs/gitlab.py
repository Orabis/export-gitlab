import gitlab

from exportgitlab.libs.color_contrast import passes


def gl_connection(user_token):
    gl = gitlab.Gitlab(url="https://git.unistra.fr", private_token=user_token)
    gl.auth()
    return gl


def get_labels_list(gitlab_project):
    gitlab_labels = gitlab_project.labels.list(get_all=True)
    gitlab_labels_dict = {}
    for label in gitlab_labels:
        accessibility_color_check = passes(label.color, "#ffffff")
        if accessibility_color_check:
            gitlab_labels_dict[label.name] = {"bg_color": label.color, "text_color": "#FFFFF", "id": label.id}
        else:
            gitlab_labels_dict[label.name] = {"bg_color": label.color, "text_color": "#000000", "id": label.id}
    return gitlab_labels_dict


def get_issues(gitlab_project, iid_filter, labels_filter, opened_closed_filter):
    if not opened_closed_filter:
        opened_closed_filter = "opened"
    params = {
        "get_all": True,
        "state": opened_closed_filter,
    }
    if iid_filter[0] != "":
        params["iids"] = iid_filter
    if labels_filter != [""]:
        params["labels"] = labels_filter
    return gitlab_project.issues.list(**params)
