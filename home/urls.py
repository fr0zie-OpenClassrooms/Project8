from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="home"),
    path("legal/", views.legal, name="legal"),
]
