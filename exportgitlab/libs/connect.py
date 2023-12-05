import gitlab


def gl_connection(useractualtoken):
    gl = gitlab.Gitlab(url="https://git.unistra.fr", private_token=useractualtoken)
    gl.auth()
    return gl
