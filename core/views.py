import datetime

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AnnouncementForm, EventForm
from .models import Announcement, Event

User = get_user_model()


@login_required
def dashboard(request):
    from attendance.models import AttendanceRecord
    from students.models import Student

    today = datetime.date.today()
    total_students = Student.objects.count()
    today_records = AttendanceRecord.objects.filter(date=today)
    attendance_percent = 0
    if today_records.exists() and total_students:
        present = today_records.filter(status=AttendanceRecord.Status.PRESENT).count()
        attendance_percent = round((present / total_students) * 100)

    try:
        from fees.models import Payment
        fees_collected = sum(p.amount for p in Payment.objects.all())
    except Exception:
        fees_collected = 0

    context = {
        "total_students": total_students,
        "total_staff": User.objects.filter(role__in=[User.Role.TEACHER, User.Role.STAFF]).count(),
        "staff_accepted": User.objects.filter(
            role__in=[User.Role.TEACHER, User.Role.STAFF], is_active=True
        ).count(),
        "attendance_percent": attendance_percent,
        "fees_collected": fees_collected,
        "fees_pending": 0,
        "announcements": Announcement.objects.all()[:5],
        "events": Event.objects.all()[:5],
    }
    return render(request, "core/dashboard.html", context)


@login_required
def coming_soon(request, module_name):
    """Generic placeholder so every sidebar link works from the start,
    even before its module is built out."""
    display_name = module_name.replace("-", " ").title()
    return render(request, "core/coming_soon.html", {"module_name": display_name})


# ---------- Announcements CRUD ----------

@login_required
def announcement_list(request):
    announcements = Announcement.objects.prefetch_related("classes").all()
    edit_forms = {a.id: AnnouncementForm(instance=a) for a in announcements}
    events = Event.objects.all()
    event_edit_forms = {e.id: EventForm(instance=e) for e in events}
    return render(request, "core/announcement_list.html", {
        "announcements": announcements,
        "create_form": AnnouncementForm(initial={"date": datetime.date.today()}),
        "edit_forms": edit_forms,
        "events": events,
        "event_create_form": EventForm(initial={"date": datetime.date.today()}),
        "event_edit_forms": event_edit_forms,
    })


@login_required
def announcement_create(request):
    if request.method == "POST":
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.created_by = request.user
            announcement.save()
            form.save_m2m()
            messages.success(request, "Announcement posted.")
        else:
            messages.error(request, "Please fix the errors and try again.")
    return redirect("announcement_list")


@login_required
def announcement_edit(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    if request.method == "POST":
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            messages.success(request, "Announcement updated.")
            return redirect("announcement_list")
        messages.error(request, "Please fix the errors and try again.")
        announcements = Announcement.objects.prefetch_related("classes").all()
        edit_forms = {a.id: AnnouncementForm(instance=a) for a in announcements}
        edit_forms[pk] = form
        return render(request, "core/announcement_list.html", {
            "announcements": announcements,
            "create_form": AnnouncementForm(initial={"date": datetime.date.today()}),
            "edit_forms": edit_forms,
            "open_edit_id": pk,
        })
    return redirect("announcement_list")


@login_required
def announcement_delete(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    if request.method == "POST":
        announcement.delete()
        messages.success(request, "Announcement deleted.")
    return redirect("announcement_list")


# ---------- Events CRUD ----------

@login_required
def event_create(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Event added.")
        else:
            messages.error(request, "Please fix the errors and try again.")
    return redirect("announcement_list")


@login_required
def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated.")
        else:
            messages.error(request, "Please fix the errors and try again.")
    return redirect("announcement_list")


@login_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        event.delete()
        messages.success(request, "Event removed.")
    return redirect("announcement_list")
