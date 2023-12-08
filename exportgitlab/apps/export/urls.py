from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("profile/", views.profile, name="profile"),
    path("profile/token_pending/", views.changetoken, name="tokenchangedpending"),
    path("projects/", views.projects, name="projects"),
    path("projects/refresh/<int:id_pj>", views.refresh, name="refreshproject"),
    path("projects/<int:id_pj>/", views.issues, name="issue_list"),
    path("projects/<int:id_pj>/download", views.download, name="download_issues"),
]
