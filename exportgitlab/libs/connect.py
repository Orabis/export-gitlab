import gitlab


def gl_connection(user_token):
    gl = gitlab.Gitlab(url="https://git.unistra.fr", private_token=user_token)
    gl.auth()
    return gl
