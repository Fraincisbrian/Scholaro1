from django.urls import path

from . import views

app_name = "staff"

urlpatterns = [
    path("", views.staff_directory, name="directory"),
    path("invite/", views.staff_invite, name="invite"),
    path("<int:pk>/edit/", views.staff_edit, name="edit"),
    path("<int:pk>/delete/", views.staff_delete, name="delete"),
    path("<int:pk>/resend/", views.staff_resend_invite, name="resend"),
    path("accept-invite/<uidb64>/<token>/", views.accept_invite, name="accept_invite"),
]
