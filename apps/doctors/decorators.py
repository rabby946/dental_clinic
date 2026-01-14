# apps/doctors/decorators.py
from django.shortcuts import redirect
from functools import wraps

def doctor_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and hasattr(request.user, 'doctor_profile'):
            return view_func(request, *args, **kwargs)
        else:
            return redirect('doctor_login')  # your login page
    return wrapper
