from django.conf import settings
from django.contrib import admin
from django.urls import include, re_path

urlpatterns = [
    re_path("admin/", admin.site.urls, name="admin"),
    re_path("^api/(?P<version>(v1))/", include("dj_rest_auth.urls")),
    re_path("^api/(?P<version>(v1))/registration/", include("dj_rest_auth.registration.urls")),
    re_path("^api/(?P<version>(v1))/", include("apps.events.urls")),
]

if settings.DEBUG:
    urlpatterns += [re_path("", include(("apps.swagger.urls", "swagger")))]
