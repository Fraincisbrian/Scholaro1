from django.urls import path

from . import views

app_name = "attendance"

urlpatterns = [
    path("", views.mark_attendance, name="mark"),
    path("save/", views.save_attendance, name="save"),
]
