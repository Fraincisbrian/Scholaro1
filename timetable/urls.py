from django.urls import path

from . import views

app_name = "timetable"

urlpatterns = [
    path("", views.timetable_view, name="view"),
    path("<int:class_id>/<str:day>/<int:period>/save/", views.slot_save, name="slot_save"),
    path("slot/<int:pk>/delete/", views.slot_delete, name="slot_delete"),
]
