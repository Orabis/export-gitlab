from functools import wraps

from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from gitlab import GitlabGetError

from exportgitlab.libs.gitlab import gl_connection
from exportgitlab.libs.utils import *


def gitlab_valid_auth_required(func):
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            try:
                user_token = get_token_or_redirect(request)
                gl = gl_connection(user_token)
            except GitlabAuthenticationError as e:
                messages.add_message(
                    request, messages.ERROR, _("Invalid gitlab token %(error_name)s") % {"error_name": e}
                )
                return redirect("user_profile")
            except GitlabGetError as e:
                messages.add_message(request, messages.ERROR, _("Invalid token %(error_name)s") % {"error_name": e})
                return redirect("user_profile")

            request.gl = gl
            return func(request, *args, **kwargs)

        return inner

    return decorator(func)
