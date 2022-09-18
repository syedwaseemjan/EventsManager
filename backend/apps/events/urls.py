from django.urls import include, re_path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"events", views.EventViewSet, basename="events")

urlpatterns = [
    re_path("", include(router.urls)),
]
