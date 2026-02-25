from django.urls import path
from . import views

app_name = 'billing'

urlpatterns = [

    # ---------- Patient payments ----------
    path(
        'pay/<int:appointment_id>/',
        views.patient_pay_init,
        name='patient_pay_init'
    ),
    path(
        'bkash/callback/',
        views.bkash_callback,
        name='bkash_callback'
    ),

    # ---------- Doctor / Staff ----------
    path(
        'doctor/charge/<int:appointment_id>/',
        views.add_charge,
        name='add_charge'
    ),
    path(
        'doctor/manual-payment/<int:appointment_id>/',
        views.add_manual_payment,
        name='add_manual_payment'
    ),
]
