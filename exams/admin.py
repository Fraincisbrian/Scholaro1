from django.contrib import admin

from .models import Exam, Mark


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ("name", "term", "academic_year", "date", "class_count")
    list_filter = ("term", "academic_year")
    filter_horizontal = ("classes",)


@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ("student", "exam", "subject", "score", "max_score", "grade")
    list_filter = ("exam", "subject")
