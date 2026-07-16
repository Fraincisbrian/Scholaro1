from django.urls import path

from . import views

app_name = "exams"

urlpatterns = [
    path("", views.exam_list, name="list"),
    path("create/", views.exam_create, name="create"),
    path("<int:pk>/edit/", views.exam_edit, name="edit"),
    path("<int:pk>/delete/", views.exam_delete, name="delete"),
    path("<int:pk>/marks/", views.enter_marks, name="enter_marks"),
    path("<int:pk>/marks/save/", views.save_marks, name="save_marks"),
]
