from django.core.exceptions import ImproperlyConfigured
from drf_yasg import openapi
from drf_yasg.app_settings import IMPORT_STRINGS, SWAGGER_DEFAULTS, AppSettings
from drf_yasg.views import get_schema_view

swagger_settings = AppSettings(
    user_settings="SWAGGER_SETTINGS", defaults=SWAGGER_DEFAULTS, import_strings=IMPORT_STRINGS
)

DEFAULT_INFO = getattr(swagger_settings, "DEFAULT_INFO", None)
if not isinstance(DEFAULT_INFO, openapi.Info):
    raise ImproperlyConfigured(
        'settings.SWAGGER_SETTINGS["DEFAULT_INFO"] should be an ' "import string pointing to an openapi.Info object"
    )


SchemaView = get_schema_view(swagger_settings.DEFAULT_INFO, public=True)
