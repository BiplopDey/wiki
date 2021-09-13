from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("add", views.newPage, name="add"),
    path("edit/<str:title>", views.edit, name = "edit")
]
