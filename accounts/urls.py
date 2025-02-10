from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),  # Add this line
    path('login/', views.login_view, name='login'),  # Add this line
    path('logout/', views.logout_view, name='logout'),  # Add this line
    path('employer/profile/', views.edit_employer_profile, name='edit_employer_profile'),
    path('jobseeker/profile/', views.edit_jobseeker_profile, name='edit_jobseeker_profile'),
    path('profile/success/', views.profile_success, name='profile_success'),
    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
