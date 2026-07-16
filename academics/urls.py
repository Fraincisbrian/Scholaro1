from django.urls import path

from . import views

app_name = "academics"

urlpatterns = [
    path("", views.class_setup, name="class_setup"),
    path("create/", views.class_create, name="class_create"),
    path("<int:pk>/edit/", views.class_edit, name="class_edit"),
    path("<int:pk>/delete/", views.class_delete, name="class_delete"),
    path("promote/", views.bulk_promote, name="bulk_promote"),

    path("<int:class_id>/subjects/create/", views.subject_create, name="subject_create"),
    path("subjects/<int:pk>/edit/", views.subject_edit, name="subject_edit"),
    path("subjects/<int:pk>/delete/", views.subject_delete, name="subject_delete"),
]
