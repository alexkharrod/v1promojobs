from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('employer/profile/', views.edit_employer_profile, name='edit_employer_profile'),
    path('jobseeker/profile/', views.edit_jobseeker_profile, name='edit_jobseeker_profile'),
    path('profile/success/', views.profile_success, name='profile_success'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('api-token-auth/', views.obtain_auth_token, name='api_token_auth'),
]
