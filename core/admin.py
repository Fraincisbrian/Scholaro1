from django.contrib import admin

from .models import Announcement, Event


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "all_school", "is_important")
    list_filter = ("all_school", "is_important")
    search_fields = ("title", "message")
    filter_horizontal = ("classes",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "time_label", "audience")
    ordering = ("date",)
