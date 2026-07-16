from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from academics.models import SchoolClass

from .forms import StudentForm
from .models import Student


def _filter_context():
    """Shared lookups so every filter/dropdown reflects Class Setup live."""
    classes = SchoolClass.objects.all()
    level_labels = dict(SchoolClass.LEVEL_CHOICES)
    used_levels = classes.values_list("level", flat=True).distinct()
    levels = [(value, level_labels.get(value, value)) for value in used_levels]
    sections = classes.values_list("section", flat=True).distinct().exclude(section="")

    classes_by_stream = SchoolClass.grouped_by_stream(classes)

    return {
        "streams": SchoolClass.Stream.choices,
        "levels": levels,
        "sections": sections,
        "classes_by_stream": classes_by_stream,
    }


@login_required
def student_list(request):
    students = Student.objects.select_related("school_class").filter(is_alumni=False)

    query = request.GET.get("q", "").strip()
    stream_filter = request.GET.get("stream", "")
    class_filter = request.GET.get("class", "")
    section_filter = request.GET.get("section", "")

    if query:
        students = students.filter(full_name__icontains=query) | students.filter(roll_number__icontains=query)
    if stream_filter:
        students = students.filter(school_class__stream=stream_filter)
    if class_filter:
        students = students.filter(school_class__level=class_filter)
    if section_filter:
        students = students.filter(school_class__section=section_filter)

    form = StudentForm()

    return render(request, "students/student_list.html", {
        "students": students.distinct(),
        "form": form,
        "query": query,
        "stream_filter": stream_filter,
        "class_filter": class_filter,
        "section_filter": section_filter,
        **_filter_context(),
    })


@login_required
def student_enroll(request):
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Student enrolled successfully.")
            return redirect("students:list")
        messages.error(request, "Please fix the errors below and try again.")
        return render(request, "students/student_list.html", {
            "students": Student.objects.select_related("school_class").filter(is_alumni=False),
            "form": form,
            "open_modal": True,
            **_filter_context(),
        })
    return redirect("students:list")


@login_required
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, "students/student_detail.html", {"student": student})


@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        student.delete()
        messages.success(request, "Student removed.")
    return redirect("students:list")
