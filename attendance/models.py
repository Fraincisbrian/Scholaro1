from django.db import models

from academics.models import SchoolClass
from students.models import Student


class AttendanceRecord(models.Model):
    class Status(models.TextChoices):
        PRESENT = "present", "Present"
        ABSENT = "absent", "Absent"
        LATE = "late", "Late"

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="attendance_records")
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, related_name="attendance_records")
    date = models.DateField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PRESENT)

    class Meta:
        unique_together = ("student", "date")
        ordering = ["-date"]

    def __str__(self):
        return f"{self.student} - {self.date} - {self.status}"
