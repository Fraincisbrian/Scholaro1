from django.contrib import admin

from .models import FeeStructure, Payment


@admin.register(FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):
    list_display = ("fee_type", "class_label", "amount")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("student", "amount", "date", "mode", "status")
    list_filter = ("mode", "status")
