from django.urls import path
from jobs.views import JobListAPIView, JobDetailAPIView, job_create, job_edit, job_list, job_detail, saved_searches, save_search, delete_saved_search

urlpatterns = [
    path('create/', job_create, name='job_create'),
    path('<int:pk>/edit/', job_edit, name='job_edit'),
    path('', job_list, name='job_list'),
    path('<int:pk>/', job_detail, name='job_detail'),
    path('saved_searches/', saved_searches, name='saved_searches'),
    path('save_search/', save_search, name='save_search'),
    path('delete_saved_search/<int:pk>/', delete_saved_search, name='delete_saved_search'),
    path('api/jobs/', JobListAPIView.as_view(), name='job_list_api'),
    path('api/jobs/<int:pk>/', JobDetailAPIView.as_view(), name='job_detail_api'),
]
