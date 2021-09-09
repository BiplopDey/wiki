from re import search
from django.urls import path

from . import views

#app_name = "entryPage"

urlpatterns = [
    path("<str:title>", views.getTitle, name="title")
   
]
