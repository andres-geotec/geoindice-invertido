from django.urls import path
from . import views

urlpatterns = [
    path("resources/", views.ResourceListView.as_view(), name="resource-list"),
]
