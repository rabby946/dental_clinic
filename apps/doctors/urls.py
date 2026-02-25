from django.urls import path
from . import views

app_name = 'doctors'

urlpatterns = [
    # Login / Logout
    path('login/', views.doctor_login, name='login'),
    path('logout/', views.doctor_logout, name='logout'),

    # Dashboard
    path('dashboard/', views.doctor_dashboard, name='dashboard'),

    # Appointments
    path('appointments/', views.appointment_list, name='appointments'),
    path('appointments/<int:pk>/', views.appointment_detail, name='appointment_detail'),

    path('dashboard/', views.doctor_dashboard, name='dashboard'),

    path('patients/search/', views.patient_search, name='patient_search'),
    path('patients/create/', views.patient_create, name='patient_create'),
    path('patients/<int:pk>/', views.patient_detail, name='patient_detail'),

]
