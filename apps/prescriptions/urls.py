from django.urls import path
from . import views

app_name = 'prescriptions'

urlpatterns = [
    path('create/<int:patient_id>/', views.prescription_create, name='create'),
    path("view/<int:pk>/", views.prescription_detail, name="detail"),
]
