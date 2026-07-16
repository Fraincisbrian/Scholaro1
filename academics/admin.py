from django.contrib import admin

from .models import SchoolClass, Subject


@admin.register(SchoolClass)
class SchoolClassAdmin(admin.ModelAdmin):
    list_display = ("level", "section", "stream", "class_teacher", "student_count")
    list_filter = ("stream", "level")


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "school_class", "teacher")
    list_filter = ("school_class",)
