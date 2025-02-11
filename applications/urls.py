from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('apply/<int:job_id>/', views.apply_for_job, name='apply_for_job'),
    path('employer/<int:job_id>/', views.employer_applications, name='employer_applications'),
    path('<int:pk>/', views.application_detail, name='application_detail'),
    path('<int:pk>/update_status/', views.update_application_status, name='update_application_status'),
    path('success/', TemplateView.as_view(template_name='applications/application_success.html'), name='application_success'),
    path('failure/', TemplateView.as_view(template_name='applications/application_failure.html'), name='application_failure'),
]
