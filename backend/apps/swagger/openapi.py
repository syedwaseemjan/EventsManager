from django.conf import settings
from drf_yasg import openapi

API_INFO = openapi.Info(
    title="EventsAPI",
    default_version=settings.CURRENT_API_VERSION,
    contact=openapi.Contact(email="engineering@api.com"),
)
