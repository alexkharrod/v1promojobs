from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.job_create, name='job_create'),
    path('<int:pk>/edit/', views.job_edit, name='job_edit'),
    path('', views.job_list, name='job_list'),
    path('<int:pk>/', views.job_detail, name='job_detail'),
    path('saved_searches/', views.saved_searches, name='saved_searches'),
    path('save_search/', views.save_search, name='save_search'),
    path('delete_saved_search/<int:pk>/', views.delete_saved_search, name='delete_saved_search'),
]
