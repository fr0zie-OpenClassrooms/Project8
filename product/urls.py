from django.urls import path
from . import views


urlpatterns = [
    path("search/", views.search, name="search"),
    path("details/<product_name>/", views.details, name="details"),
    path("substitutes/", views.substitutes, name="substitutes"),
    path("save/", views.save, name="save"),
    path("delete/", views.delete, name="delete"),
]
