from django.urls import path

from . import views

app_name = "fees"

urlpatterns = [
    path("", views.fee_management, name="management"),
    path("structure/create/", views.fee_structure_create, name="structure_create"),
    path("structure/<int:pk>/edit/", views.fee_structure_edit, name="structure_edit"),
    path("structure/<int:pk>/delete/", views.fee_structure_delete, name="structure_delete"),
    path("student/<int:student_id>/pay/", views.record_payment, name="record_payment"),
    path("payment/<int:pk>/edit/", views.payment_edit, name="payment_edit"),
    path("payment/<int:pk>/delete/", views.payment_delete, name="payment_delete"),
    path("student/<int:student_id>/history/", views.payment_history, name="payment_history"),
    path("receipt/<int:payment_id>/", views.receipt, name="receipt"),
    path("defaulters/", views.fee_defaulters, name="defaulters"),
]
