from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("profile/", views.profile, name="profile"),
    path("profile/token_pending/", views.changetoken, name="tokenchangedpending"),
    path("projects/", views.projects, name="projects"),
]
