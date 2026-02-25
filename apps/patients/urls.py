from django.urls import path
from . import views

app_name = 'patients'

urlpatterns = [
    # Login / Logout
    path('login/', views.patient_login, name='login'),
    path('logout/', views.patient_logout, name='logout'),

    # Dashboard
    path('dashboard/', views.patient_dashboard, name='dashboard'),

    # Profile
    path('profile/', views.patient_profile_update, name='profile'),

    # Prescriptions
    path('prescriptions/', views.prescription_list, name='prescription_list'),
    path('prescriptions/<int:pk>/', views.prescription_detail, name='prescription_detail'),
    path('prescriptions/<int:pk>/download/', views.prescription_download, name='prescription_download'),


    # Payments
    path('payments/', views.payment_list, name='payments'),
    path('payments/<int:pk>/', views.payment_detail, name='payment_detail'),

    # Appointments
    path('appointments/', views.appointment_list, name='appointments'),
    path('appointments/<int:pk>/', views.appointment_detail, name='appointment_detail'),

    path('change_password/', views.change_password, name='change_password'),

    # Documents
    path('documents/', views.documents, name='documents'),
    path('documents/<int:pk>/', views.document_details, name='document_details'),
]
