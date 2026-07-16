from django.contrib import admin

from .models import TimetableEntry


@admin.register(TimetableEntry)
class TimetableEntryAdmin(admin.ModelAdmin):
    list_display = ("school_class", "day", "period", "subject", "teacher")
    list_filter = ("school_class", "day")
