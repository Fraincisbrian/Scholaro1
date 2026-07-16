from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model for SchoolWise.

    Extends Django's built-in user with a role field so the same login
    system can later serve Admins, Teachers, and other Staff — while the
    current build focuses on the Admin experience.
    """

    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        TEACHER = "teacher", "Teacher"
        STAFF = "staff", "Staff"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.ADMIN)
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    def __str__(self):
        full_name = self.get_full_name()
        return full_name if full_name else self.username

    @property
    def is_admin_role(self):
        return self.role == self.Role.ADMIN
