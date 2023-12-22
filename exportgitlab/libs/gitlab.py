import gitlab


def gl_connection(user_token):
    gl = gitlab.Gitlab(url="https://git.unistra.fr", private_token=user_token)
    gl.auth()
    return gl


def get_labels_list(gitlab_project):
    gitlab_labels = gitlab_project.labels.list(get_all=True)
    gitlab_labels_dict = {label.name: label.color for label in gitlab_labels}
    return gitlab_labels_dict


def get_issues(gitlab_project, iid_filter, labels_filter, opened_closed_filter):
    params = {
        "get_all": True,
        "state": opened_closed_filter,
    }
    if iid_filter[0] != "":
        params["iids"] = iid_filter
    elif labels_filter != [None]:
        params["labels"] = labels_filter
    return gitlab_project.issues.list(**params)
