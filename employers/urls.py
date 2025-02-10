from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.employer_profile_create, name='employer_profile_create'),
    path('<int:pk>/edit/', views.employer_profile_edit, name='employer_profile_edit'),
    path('<int:pk>/', views.employer_profile_detail, name='employer_profile_detail'),
]
