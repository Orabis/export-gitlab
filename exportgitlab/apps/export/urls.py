from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("profile/", views.user_profile, name="user_profile"),
    path("profile/token_pending/", views.user_change_token, name="user_change_token"),
    path("projects/", views.list_all_projects_homepage, name="list_all_projects_homepage"),
    path("projects/refresh/<int:id_pj>/", views.refresh_project, name="refresh_project"),
    path("projects/<int:id_pj>/selection/", views.list_all_issues, name="list_all_issues"),
    path("projects/<int:id_pj>/download/", views.download_report_issues, name="download_report_issues"),
    path("projects/<int:id_pj>/", views.project_info, name="project_info"),
    path("projects/<int:id_pj>/issues/", views.issues_info, name="issues_info"),
    path("projects/<int:id_pj>/labels/", views.labels_info, name="labels_info"),
    path("accounts/login/", views.login_view, name="login"),
    path("accounts/logout/", views.logout_view, name="logout"),
]
