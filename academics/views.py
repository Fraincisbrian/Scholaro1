from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from students.models import Student

from .forms import SchoolClassForm, SubjectForm
from .models import SchoolClass, Subject


@login_required
def class_setup(request):
    classes = SchoolClass.objects.select_related("class_teacher").prefetch_related("subjects__teacher").all()
    class_edit_forms = {c.id: SchoolClassForm(instance=c) for c in classes}
    subject_forms = {c.id: SubjectForm() for c in classes}
    subject_edit_forms = {
        subj.id: SubjectForm(instance=subj)
        for c in classes for subj in c.subjects.all()
    }

    return render(request, "academics/class_setup.html", {
        "classes": classes,
        "create_form": SchoolClassForm(),
        "class_edit_forms": class_edit_forms,
        "subject_forms": subject_forms,
        "subject_edit_forms": subject_edit_forms,
        "levels_by_stream": {
            SchoolClass.Stream.TECHNICAL: SchoolClass.TECHNICAL_LEVELS,
            SchoolClass.Stream.GRAMMAR: SchoolClass.GRAMMAR_LEVELS,
        },
    })


@login_required
def class_create(request):
    if request.method == "POST":
        form = SchoolClassForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Class added.")
        else:
            messages.error(request, "Please fix the errors and try again.")
    return redirect("academics:class_setup")


@login_required
def class_edit(request, pk):
    school_class = get_object_or_404(SchoolClass, pk=pk)
    if request.method == "POST":
        form = SchoolClassForm(request.POST, instance=school_class)
        if form.is_valid():
            form.save()
            messages.success(request, "Class updated.")
        else:
            messages.error(request, "Please fix the errors and try again.")
    return redirect("academics:class_setup")


@login_required
def class_delete(request, pk):
    school_class = get_object_or_404(SchoolClass, pk=pk)
    if request.method == "POST":
        school_class.delete()
        messages.success(request, "Class removed.")
    return redirect("academics:class_setup")


@login_required
def bulk_promote(request):
    if request.method == "POST":
        source_id = request.POST.get("source_class")
        destination = request.POST.get("destination_class")
        source = get_object_or_404(SchoolClass, pk=source_id)
        students = Student.objects.filter(school_class=source)

        if destination == "alumni":
            count = students.update(is_alumni=True, school_class=None)
            messages.success(request, f"Promoted {count} student(s) to Alumni.")
        elif destination:
            dest = get_object_or_404(SchoolClass, pk=destination)
            count = students.update(school_class=dest)
            messages.success(request, f"Promoted {count} student(s) to {dest}.")
        else:
            messages.error(request, "Please choose a destination class.")

    return redirect("academics:class_setup")


# ---------- Subjects (per class) ----------

@login_required
def subject_create(request, class_id):
    school_class = get_object_or_404(SchoolClass, pk=class_id)
    if request.method == "POST":
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.school_class = school_class
            subject.save()
            messages.success(request, "Subject assigned.")
        else:
            messages.error(request, "Please fix the errors and try again.")
    return redirect("academics:class_setup")


@login_required
def subject_edit(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == "POST":
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            messages.success(request, "Subject updated.")
    return redirect("academics:class_setup")


@login_required
def subject_delete(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == "POST":
        subject.delete()
        messages.success(request, "Subject removed.")
    return redirect("academics:class_setup")
