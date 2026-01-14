from django.urls import path
from . import views

app_name = 'doctors'

urlpatterns = [
    # Login / Logout
    path('login/', views.doctor_login, name='login'),
    path('logout/', views.DoctorLogoutView.as_view(), name='logout'),

    # Dashboard
    path('dashboard/', views.doctor_dashboard, name='dashboard'),

    # Appointments
    path('appointments/', views.appointment_list, name='appointments'),
    path('appointments/<int:pk>/', views.appointment_detail, name='appointment_detail'),

    # Patients
    path('patients/', views.patient_list, name='patients'),
    path('patients/<int:pk>/', views.patient_detail, name='patient_detail'),
]
