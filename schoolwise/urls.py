"""URL configuration for the Scholaro project."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "Scholaro Administration"
admin.site.site_title = "Scholaro Admin"
admin.site.index_title = "Site Administration"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("students/", include("students.urls")),
    path("attendance/", include("attendance.urls")),
    path("fees/", include("fees.urls")),
    path("exams/", include("exams.urls")),
    path("timetable/", include("timetable.urls")),
    path("staff/", include("staff.urls")),
    path("class-setup/", include("academics.urls")),
    path("", include("core.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
