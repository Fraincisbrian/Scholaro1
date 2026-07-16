from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from academics.models import SchoolClass, Subject
from students.models import Student

from .forms import ExamForm
from .models import Exam, Mark


@login_required
def exam_list(request):
    exams = Exam.objects.prefetch_related("classes", "marks").all()
    edit_forms = {e.id: ExamForm(instance=e, initial={"classes": e.classes.all()}) for e in exams}
    selected_classes_by_exam = {e.id: set(e.classes.values_list("id", flat=True)) for e in exams}

    return render(request, "exams/exam_list.html", {
        "exams": exams,
        "create_form": ExamForm(),
        "edit_forms": edit_forms,
        "terms": Exam.Term.choices,
        "classes_by_stream": SchoolClass.grouped_by_stream(),
        "selected_classes_by_exam": selected_classes_by_exam,
    })


@login_required
def exam_create(request):
    if request.method == "POST":
        form = ExamForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Exam created.")
        else:
            messages.error(request, "Please fix the errors and try again.")
    return redirect("exams:list")


@login_required
def exam_edit(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    if request.method == "POST":
        form = ExamForm(request.POST, instance=exam)
        if form.is_valid():
            form.save()
            messages.success(request, "Exam updated.")
        else:
            messages.error(request, "Please fix the errors and try again.")
    return redirect("exams:list")


@login_required
def exam_delete(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    if request.method == "POST":
        exam.delete()
        messages.success(request, "Exam removed.")
    return redirect("exams:list")


@login_required
def enter_marks(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    classes = exam.classes.all()

    class_id = request.GET.get("school_class") or ""
    subject_id = request.GET.get("subject") or ""

    subjects = Subject.objects.filter(school_class_id=class_id) if class_id else Subject.objects.none()

    students = []
    existing = {}
    if class_id and subject_id:
        students = Student.objects.filter(school_class_id=class_id, is_alumni=False).order_by("roll_number", "full_name")
        existing = {
            mark.student_id: mark
            for mark in Mark.objects.filter(exam=exam, subject_id=subject_id)
        }

    return render(request, "exams/enter_marks.html", {
        "exam": exam,
        "classes_by_stream": SchoolClass.grouped_by_stream(classes),
        "class_id": str(class_id),
        "subjects": subjects,
        "subject_id": str(subject_id),
        "students": students,
        "existing": existing,
    })


@login_required
def save_marks(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    if request.method != "POST":
        return redirect("exams:enter_marks", pk=pk)

    class_id = request.POST.get("school_class")
    subject_id = request.POST.get("subject")
    subject = get_object_or_404(Subject, pk=subject_id)
    max_score = request.POST.get("max_score") or 100
    students = Student.objects.filter(school_class_id=class_id, is_alumni=False)

    saved = 0
    for student in students:
        raw_score = request.POST.get(f"score_{student.id}", "").strip()
        if raw_score == "":
            continue
        try:
            score = float(raw_score)
        except ValueError:
            continue
        remarks = request.POST.get(f"remarks_{student.id}", "").strip()
        Mark.objects.update_or_create(
            exam=exam, student=student, subject=subject,
            defaults={"score": score, "max_score": max_score, "remarks": remarks},
        )
        saved += 1

    messages.success(request, f"Marks saved for {saved} student(s).")
    return redirect(f"/exams/{pk}/marks/?school_class={class_id}&subject={subject_id}")
