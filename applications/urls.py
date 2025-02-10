from django.urls import path
from . import views

urlpatterns = [
    path('apply/<int:job_id>/', views.apply_for_job, name='apply_for_job'),
    path('employer/<int:job_id>/', views.employer_applications, name='employer_applications'),
    path('<int:pk>/', views.application_detail, name='application_detail'),
    path('<int:pk>/update_status/', views.update_application_status, name='update_application_status'),
]
