from django.urls import path

from . import views

urlpatterns = [
    path("swagger<str:format>", views.SchemaView.without_ui(cache_timeout=0), name="schema-json"),
    path("swagger/", views.SchemaView.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", views.SchemaView.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
