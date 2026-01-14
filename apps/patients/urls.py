from django.urls import path
from . import views

app_name = 'patients'

urlpatterns = [
    path('login/', views.PatientLoginView.as_view(), name='login'),
    path('logout/', views.PatientLogoutView.as_view(), name='logout'),
    path('dashboard/', views.PatientDashboardView.as_view(), name='dashboard'),
    path('profile/', views.PatientProfileUpdateView.as_view(), name='profile'),
    path('prescriptions/', views.PrescriptionListView.as_view(), name='prescription_list'),
    path('prescriptions/<int:pk>/', views.PrescriptionDetailView.as_view(), name='prescription_detail'),
    path('payments/', views.PaymentListView.as_view(), name='payments'),
    path('payments/<int:pk>/', views.PaymentDetailView.as_view(), name='payment_detail'),
]
