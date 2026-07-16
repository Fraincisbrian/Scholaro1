from django.contrib.auth.views import LoginView as DjangoLoginView
from django.urls import reverse_lazy

from .forms import SchoolWiseAuthenticationForm


class LoginView(DjangoLoginView):
    """Matches the SchoolWise 'Welcome back' login screen."""

    template_name = "registration/login.html"
    authentication_form = SchoolWiseAuthenticationForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("dashboard")
