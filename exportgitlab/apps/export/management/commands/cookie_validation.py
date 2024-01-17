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
            msg = "Le jeton de session de GitLab a expiré, rendant impossible la récupération des images liées aux issues sans l'utilisation du cookie. Afin d'en définir un nouveau, veuillez redéployer l'application en incluant le paramètre suivant : `gitlab_session_cookie`."
            title = "Session Gitlab expirée"
            mail = EmailMessage(f"[Export-Gitlab] {title}", msg, settings.DEFAULT_FROM_EMAIL, settings.USERS_EMAILS)
            mail.send()
            logger = logging.getLogger(__name__)
            logger.error("Le cookie de la session Gitlab a expirée")
