"""Red Dragon MUD web URLs."""

from django.urls import path, include

urlpatterns = [
    path("", include("evennia.web.urls")),
]
