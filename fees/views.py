from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from academics.models import SchoolClass
from students.models import Student

from .forms import FeeStructureForm, PaymentForm
from .models import FeeStructure, Payment


def _student_fee_rows(students):
    rows = []
    for student in students:
        total = FeeStructure.total_for_class(student.school_class) if student.school_class else Decimal("0")
        paid = sum((p.amount for p in student.payments.filter(status=Payment.Status.PAID)), start=Decimal("0"))
        balance = total - paid
        if total == 0:
            status = "No Fee Set"
        elif balance <= 0:
            status = "Paid"
        elif paid > 0:
            status = "Partial"
        else:
            status = "Unpaid"
        rows.append({
            "student": student, "total": total, "paid": paid, "balance": balance, "status": status,
            "has_payments": student.payments.exists(),
        })
    return rows


@login_required
def fee_management(request):
    structures = FeeStructure.objects.select_related("school_class").all()
    edit_forms = {f.id: FeeStructureForm(instance=f) for f in structures}
    students = Student.objects.select_related("school_class").filter(is_alumni=False)
    fee_rows = _student_fee_rows(students)

    payments_by_student = {
        row["student"].id: row["student"].payments.all()
        for row in fee_rows if row["has_payments"]
    }
    payment_edit_forms = {
        payment.id: PaymentForm(instance=payment)
        for payments in payments_by_student.values()
        for payment in payments
    }

    return render(request, "fees/fee_management.html", {
        "structures": structures,
        "structure_create_form": FeeStructureForm(),
        "structure_edit_forms": edit_forms,
        "fee_rows": fee_rows,
        "payment_form": PaymentForm(),
        "payments_by_student": payments_by_student,
        "payment_edit_forms": payment_edit_forms,
        "active_tab": request.GET.get("tab", "collection"),
    })


@login_required
def fee_structure_create(request):
    if request.method == "POST":
        form = FeeStructureForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Fee structure saved.")
        else:
            messages.error(request, "Please fix the errors and try again.")
    return redirect(f"/fees/?tab=structure")


@login_required
def fee_structure_edit(request, pk):
    structure = get_object_or_404(FeeStructure, pk=pk)
    if request.method == "POST":
        form = FeeStructureForm(request.POST, instance=structure)
        if form.is_valid():
            form.save()
            messages.success(request, "Fee structure updated.")
    return redirect(f"/fees/?tab=structure")


@login_required
def fee_structure_delete(request, pk):
    structure = get_object_or_404(FeeStructure, pk=pk)
    if request.method == "POST":
        structure.delete()
        messages.success(request, "Fee structure removed.")
    return redirect(f"/fees/?tab=structure")


@login_required
def record_payment(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.student = student
            payment.save()
            messages.success(request, "Payment recorded.")
            return redirect("fees:receipt", payment_id=payment.id)
        messages.error(request, "Please fix the errors and try again.")
    return redirect("fees:management")


@login_required
def payment_edit(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    if request.method == "POST":
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            messages.success(request, "Payment updated.")
        else:
            messages.error(request, "Please fix the errors and try again.")
    return redirect("fees:management")


@login_required
def payment_delete(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    if request.method == "POST":
        payment.delete()
        messages.success(request, "Payment removed.")
    return redirect("fees:management")


@login_required
def payment_history(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    payments = student.payments.all()
    return render(request, "fees/payment_history.html", {"student": student, "payments": payments})


@login_required
def receipt(request, payment_id):
    payment = get_object_or_404(Payment, pk=payment_id)
    total_paid = sum((p.amount for p in payment.student.payments.filter(status=Payment.Status.PAID)), start=Decimal("0"))
    return render(request, "fees/receipt.html", {"payment": payment, "total_paid": total_paid})


@login_required
def fee_defaulters(request):
    students = Student.objects.select_related("school_class").filter(is_alumni=False)
    rows = [r for r in _student_fee_rows(students) if r["status"] in ("Unpaid", "Partial")]
    return render(request, "fees/fee_defaulters.html", {"rows": rows})
