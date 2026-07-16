import re

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .forms import AcceptInviteForm, StaffEditForm, StaffInviteForm
from .models import StaffProfile

User = get_user_model()


def _unique_username(first_name, last_name, email):
    base = re.sub(r"[^a-z0-9.]", "", f"{first_name}.{last_name}".lower()) or email.split("@")[0]
    username = base
    n = 1
    while User.objects.filter(username=username).exists():
        n += 1
        username = f"{base}{n}"
    return username


def _send_invite_email(request, user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    accept_url = request.build_absolute_uri(f"/staff/accept-invite/{uid}/{token}/")
    send_mail(
        subject="You're invited to Scholaro",
        message=(
            f"Hi {user.first_name},\n\n"
            f"You've been added as {user.get_role_display()} on Scholaro.\n"
            f"Set your password to activate your account:\n{accept_url}\n\n"
            f"If you weren't expecting this, you can ignore this email."
        ),
        from_email=None,
        recipient_list=[user.email],
        fail_silently=True,
    )


@login_required
def staff_directory(request):
    query = request.GET.get("q", "").strip()
    staff_users = User.objects.filter(role__in=[User.Role.TEACHER, User.Role.STAFF]).select_related("staff_profile")
    if query:
        staff_users = staff_users.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(email__icontains=query)
        )
    staff_users = staff_users.order_by("first_name", "last_name")
    edit_forms = {
        u.id: StaffEditForm(initial={
            "first_name": u.first_name, "last_name": u.last_name, "phone": u.phone,
            "role": u.role, "designation": getattr(u.staff_profile, "designation", ""),
        }) for u in staff_users
    }

    return render(request, "staff/staff_directory.html", {
        "staff_users": staff_users,
        "invite_form": StaffInviteForm(),
        "edit_forms": edit_forms,
        "query": query,
    })


@login_required
def staff_invite(request):
    if request.method == "POST":
        form = StaffInviteForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = _unique_username(data["first_name"], data["last_name"], data["email"])
            user = User.objects.create_user(
                username=username,
                email=data["email"],
                first_name=data["first_name"],
                last_name=data["last_name"],
                phone=data.get("phone", ""),
                role=data["role"],
                is_active=False,
            )
            user.set_unusable_password()
            user.save()
            StaffProfile.objects.create(
                user=user, designation=data.get("designation", ""), invited_by=request.user,
            )
            _send_invite_email(request, user)
            messages.success(request, f"Invite sent to {data['email']}.")
        else:
            messages.error(request, "Please fix the errors and try again.")
    return redirect("staff:directory")


@login_required
def staff_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = StaffEditForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user.first_name = data["first_name"]
            user.last_name = data["last_name"]
            user.phone = data.get("phone", "")
            user.role = data["role"]
            user.save()
            profile, _ = StaffProfile.objects.get_or_create(user=user)
            profile.designation = data.get("designation", "")
            profile.save()
            messages.success(request, "Staff member updated.")
        else:
            messages.error(request, "Please fix the errors and try again.")
    return redirect("staff:directory")


@login_required
def staff_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        user.delete()
        messages.success(request, "Staff member removed.")
    return redirect("staff:directory")


@login_required
def staff_resend_invite(request, pk):
    user = get_object_or_404(User, pk=pk, is_active=False)
    if request.method == "POST":
        _send_invite_email(request, user)
        messages.success(request, f"Invite re-sent to {user.email}.")
    return redirect("staff:directory")


def accept_invite(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    valid = user is not None and default_token_generator.check_token(user, token)

    if not valid:
        return render(request, "staff/accept_invite.html", {"invalid": True})

    if request.method == "POST":
        form = AcceptInviteForm(request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data["password1"])
            user.is_active = True
            user.save()
            messages.success(request, "Your account is active. You can now sign in.")
            return redirect("login")
    else:
        form = AcceptInviteForm()

    return render(request, "staff/accept_invite.html", {"form": form, "user_obj": user, "invalid": False})
