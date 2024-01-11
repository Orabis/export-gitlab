import logging

import requests
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Make a request to git.unistra with the gitlab session cookie, refreshing his availability"

    """
    A manage command to send a request to git.unistra for refreshing the same gitlab session cookie.
    If the cookie expire Export-Gitlab app can't retrieve the images from issues and a mail will be sent
    """

    def handle(self, *args, **kwargs):
        r = requests.get(
            "https://git.unistra.fr/api/v4/user",
            headers={"Cookie": f"_gitlab_session={settings.GITLAB_SESSION_COOKIE}"},
        )
        if r.status_code != 200:
            msg = "Le jeton de session de gitlab a expiré, il est impossible de récupérer les images des issues sans le cookie. Pour en définir un nouveau veuillez redéployer l'application avec ce paramètre : gitlab_session_cookie"
            title = "Session Gitlab expiré"
            mail = EmailMessage(f"[Export-Gitlab] {title}", msg, settings.DEFAULT_FROM_EMAIL, settings.USERS_EMAILS)
            mail.send()
            logger = logging.getLogger(__name__)
            logger.error("Le cookie gitlab a expiré")
