from django.contrib import admin

from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("roll_number", "full_name", "school_class", "primary_phone")
    list_filter = ("school_class",)
    search_fields = ("full_name", "roll_number")
