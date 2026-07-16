from django.db import models

from academics.models import SchoolClass


class Student(models.Model):
    class Gender(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"
        OTHER = "other", "Other"

    full_name = models.CharField(max_length=200)
    roll_number = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=Gender.choices, default=Gender.MALE)
    school_class = models.ForeignKey(
        SchoolClass, on_delete=models.SET_NULL, null=True, blank=True, related_name="students"
    )
    profile_photo = models.ImageField(upload_to="students/", blank=True, null=True)
    address = models.CharField(max_length=255, blank=True)

    # Parent details
    father_name = models.CharField(max_length=150, blank=True)
    mother_name = models.CharField(max_length=150, blank=True)
    primary_phone = models.CharField(max_length=20)
    secondary_phone = models.CharField(max_length=20, blank=True)
    parent_email = models.EmailField(blank=True)

    is_alumni = models.BooleanField(default=False, help_text="True once promoted to 'Alumni' — keeps records, hides from active directories.")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["roll_number", "full_name"]

    def __str__(self):
        return self.full_name
