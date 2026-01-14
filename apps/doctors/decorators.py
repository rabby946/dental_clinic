from django.shortcuts import redirect
from functools import wraps

def doctor_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Allow if user is authenticated and is_staff (or superuser)
        if request.user.is_authenticated and request.user.is_staff:
            return view_func(request, *args, **kwargs)
        # Otherwise, redirect to doctor login
        return redirect('doctors:login')
    return wrapper
