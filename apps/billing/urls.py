from django.urls import path
from . import views

app_name = 'billing'

urlpatterns = [

    # ---------- Patient payments ----------
    path(
        'pay/<int:appointment_id>/',
        views.patient_init,
        name='patient_init'
    ),
    path(
        'bkash/callback/',
        views.bkash_callback,
        name='bkash_callback'
    ),

    # ---------- Doctor / Staff ----------
    # billing/urls.py
    path(
        'patient/<int:patient_id>/billing/',
        views.patient_billing,
        name='patient_billing'
    ),
]
