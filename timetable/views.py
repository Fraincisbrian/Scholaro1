from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from academics.models import SchoolClass

from .forms import TimetableSlotForm
from .models import TimetableEntry


@login_required
def timetable_view(request):
    classes = SchoolClass.objects.all()
    class_id = request.GET.get("school_class") or ""

    grid = {}
    slot_forms = {}
    school_class = None

    if class_id:
        school_class = get_object_or_404(SchoolClass, pk=class_id)
        entries = {
            (e.day, e.period): e
            for e in TimetableEntry.objects.filter(school_class=school_class).select_related("subject", "teacher")
        }
        for day, _ in TimetableEntry.Day.choices:
            row = {}
            form_row = {}
            for period, _ in TimetableEntry.PERIOD_CHOICES:
                entry = entries.get((day, period))
                row[period] = entry
                form_row[period] = TimetableSlotForm(instance=entry, school_class=school_class)
            grid[day] = row
            slot_forms[day] = form_row

    return render(request, "timetable/timetable.html", {
        "classes_by_stream": SchoolClass.grouped_by_stream(classes),
        "class_id": str(class_id),
        "school_class": school_class,
        "days": TimetableEntry.Day.choices,
        "periods": TimetableEntry.PERIOD_CHOICES,
        "grid": grid,
        "slot_forms": slot_forms,
    })


@login_required
def slot_save(request, class_id, day, period):
    school_class = get_object_or_404(SchoolClass, pk=class_id)
    instance = TimetableEntry.objects.filter(school_class=school_class, day=day, period=period).first()

    if request.method == "POST":
        if request.POST.get("clear_slot"):
            if instance:
                instance.delete()
                messages.success(request, "Slot cleared.")
        else:
            form = TimetableSlotForm(request.POST, instance=instance, school_class=school_class)
            if form.is_valid():
                entry = form.save(commit=False)
                entry.school_class = school_class
                entry.day = day
                entry.period = period
                entry.save()
                messages.success(request, "Timetable slot saved.")
            else:
                messages.error(request, "Please fix the errors and try again.")

    return redirect(f"/timetable/?school_class={class_id}")


@login_required
def slot_delete(request, pk):
    entry = get_object_or_404(TimetableEntry, pk=pk)
    class_id = entry.school_class_id
    if request.method == "POST":
        entry.delete()
        messages.success(request, "Slot cleared.")
    return redirect(f"/timetable/?school_class={class_id}")
