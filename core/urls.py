from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("module/<str:module_name>/", views.coming_soon, name="coming_soon"),

    path("announcements/", views.announcement_list, name="announcement_list"),
    path("announcements/create/", views.announcement_create, name="announcement_create"),
    path("announcements/<int:pk>/edit/", views.announcement_edit, name="announcement_edit"),
    path("announcements/<int:pk>/delete/", views.announcement_delete, name="announcement_delete"),

    path("events/create/", views.event_create, name="event_create"),
    path("events/<int:pk>/edit/", views.event_edit, name="event_edit"),
    path("events/<int:pk>/delete/", views.event_delete, name="event_delete"),
]
