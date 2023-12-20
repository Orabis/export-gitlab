from functools import wraps

from django.shortcuts import redirect

from exportgitlab.libs.connect import gl_connection
from exportgitlab.libs.utils import *


def gitlab_valid_auth_required(func):
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            try:
                user_token = get_token_or_redirect(request)
                gl = gl_connection(user_token)
            except GitlabAuthenticationError:
                return redirect("user_profile")
            request.gl = gl
            return func(request, *args, **kwargs)

        return inner

    return decorator(func)
