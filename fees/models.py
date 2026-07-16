from django.db import models

from academics.models import SchoolClass
from students.models import Student


class FeeStructure(models.Model):
    """A fee type + amount, either for a specific class or 'All Classes'."""

    fee_type = models.CharField(max_length=100)
    school_class = models.ForeignKey(
        SchoolClass, on_delete=models.CASCADE, null=True, blank=True,
        related_name="fee_structures",
        help_text="Leave blank for 'All Classes'.",
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ["fee_type"]

    def __str__(self):
        return f"{self.fee_type} ({self.class_label})"

    @property
    def class_label(self):
        return str(self.school_class) if self.school_class else "All"

    @classmethod
    def total_for_class(cls, school_class):
        """Sum of all applicable fee structures (class-specific + All Classes)."""
        qs = cls.objects.filter(models.Q(school_class=school_class) | models.Q(school_class__isnull=True))
        return sum((f.amount for f in qs), start=0)


class Payment(models.Model):
    class Mode(models.TextChoices):
        CASH = "cash", "Cash"
        ONLINE = "online", "Online Transfer"
        CARD = "card", "Card"
        CHEQUE = "cheque", "Cheque"

    class Status(models.TextChoices):
        PAID = "paid", "Paid"
        PENDING = "pending", "Pending"

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    mode = models.CharField(max_length=10, choices=Mode.choices, default=Mode.CASH)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PAID)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "-id"]

    def __str__(self):
        return f"{self.student} - ₹{self.amount} ({self.date})"

    @property
    def receipt_number(self):
        return f"RCPT-{self.id:05d}"
