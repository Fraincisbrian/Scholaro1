from django.conf import settings
from django.db import models


class StaffProfile(models.Model):
    """
    Extra staff-only info layered on top of the core User model (which
    already carries role/phone/avatar). Keeps User itself app-agnostic,
    matching how other apps attach to User via FK rather than editing it.
    """

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="staff_profile")
    designation = models.CharField(max_length=100, blank=True, help_text="e.g. Mathematics Teacher, Accountant")
    invited_at = models.DateTimeField(auto_now_add=True)
    invited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="staff_invited",
    )

    def __str__(self):
        return f"{self.user} ({self.designation or self.user.get_role_display()})"
