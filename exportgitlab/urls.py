from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from .views import home

admin.autodiscover()

urlpatterns = [
    # Examples:
    path("", home, name="home"),
    # path('app/', include('apps.app.urls')),
    path("admin/", admin.site.urls),
    path("cas/", include("django_cas.urls")),
    path("profile/", include("exportgitlab.apps.export.urls")),
]

# debug toolbar for dev
if settings.DEBUG and "debug_toolbar" in settings.INSTALLED_APPS:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
