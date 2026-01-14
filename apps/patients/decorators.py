
from pyexpat.errors import messages
from django.shortcuts import redirect
from functools import wraps

from django.contrib.auth.models import User
from django.views.generic import TemplateView, ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

def patient_required(view_func):
    """Decorator to allow only Patient group users"""
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.groups.filter(name='Patient').exists():
            return view_func(request, *args, **kwargs)
        messages.error(request, "You must be logged in as a Patient to access this page.")
        return redirect('/')
    return wrapper

class PatientRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.groups.filter(name='Patient').exists()