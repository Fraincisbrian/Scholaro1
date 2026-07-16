import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from academics.models import SchoolClass
from students.models import Student

from .models import AttendanceRecord


@login_required
def mark_attendance(request):
    selected_date = request.GET.get("date") or datetime.date.today().isoformat()
    stream = request.GET.get("stream") or ""
    class_id = request.GET.get("school_class") or ""

    classes = SchoolClass.objects.filter(stream=stream) if stream else SchoolClass.objects.none()

    students = []
    existing = {}
    if class_id:
        students = Student.objects.filter(school_class_id=class_id).order_by("roll_number")
        existing = {
            rec.student_id: rec.status
            for rec in AttendanceRecord.objects.filter(date=selected_date, school_class_id=class_id)
        }

    return render(request, "attendance/mark_attendance.html", {
        "streams": SchoolClass.Stream.choices,
        "stream": stream,
        "classes": classes,
        "selected_date": selected_date,
        "class_id": str(class_id),
        "students": students,
        "existing": existing,
        "statuses": AttendanceRecord.Status.choices,
    })


@login_required
def save_attendance(request):
    if request.method != "POST":
        return redirect("attendance:mark")

    selected_date = request.POST.get("date")
    class_id = request.POST.get("school_class")
    students = Student.objects.filter(school_class_id=class_id)

    saved = 0
    for student in students:
        status = request.POST.get(f"status_{student.id}", AttendanceRecord.Status.PRESENT)
        AttendanceRecord.objects.update_or_create(
            student=student, date=selected_date,
            defaults={"school_class_id": class_id, "status": status},
        )
        saved += 1

    messages.success(request, f"Attendance saved for {saved} student(s).")
    stream = request.POST.get("stream", "")
    return redirect(f"/attendance/?date={selected_date}&stream={stream}&school_class={class_id}")
