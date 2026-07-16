from django.db import models

from academics.models import SchoolClass, Subject
from students.models import Student


class Exam(models.Model):
    """
    A single exam sitting (e.g. "Mid-Term Exam", First Term, 2025/2026),
    scoped to one or more classes. Marks are entered per student per
    subject against this exam.
    """

    class Term(models.TextChoices):
        FIRST = "first", "First Term"
        SECOND = "second", "Second Term"
        THIRD = "third", "Third Term"

    name = models.CharField(max_length=150, help_text="e.g. Mid-Term Exam, End of Year Exam")
    term = models.CharField(max_length=10, choices=Term.choices)
    academic_year = models.CharField(max_length=20, help_text="e.g. 2025/2026")
    classes = models.ManyToManyField(SchoolClass, related_name="exams", blank=True)
    date = models.DateField(null=True, blank=True, help_text="Start date of the exam (optional).")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-academic_year", "-created_at"]

    def __str__(self):
        return f"{self.name} - {self.get_term_display()} ({self.academic_year})"

    @property
    def class_count(self):
        return self.classes.count()

    def marks_entered_count(self):
        return self.marks.count()


class Mark(models.Model):
    """A single student's score for one subject, for one exam."""

    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="marks")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="marks")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="marks")
    score = models.DecimalField(max_digits=5, decimal_places=2)
    max_score = models.DecimalField(max_digits=5, decimal_places=2, default=100)
    remarks = models.CharField(max_length=100, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["student__roll_number", "student__full_name"]
        unique_together = ("exam", "student", "subject")

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.score}/{self.max_score}"

    @property
    def percentage(self):
        if not self.max_score:
            return 0
        return round((self.score / self.max_score) * 100, 1)

    @property
    def grade(self):
        pct = self.percentage
        if pct >= 80:
            return "A"
        if pct >= 70:
            return "B"
        if pct >= 60:
            return "C"
        if pct >= 50:
            return "D"
        return "F"
