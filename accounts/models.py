from django.contrib.auth.models import AbstractUser  # Import the AbstractUser model
from django.db import models  # Import the models module

class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    """
    USER_TYPE_CHOICES = (
        ("employer", "Employer"),  # Choice for Employer user type
        ("jobseeker", "Job Seeker"),  # Choice for Job Seeker user type
    )
    user_type = models.CharField(
        max_length=10,  # Maximum length for user_type field
        choices=USER_TYPE_CHOICES,  # Choices for user_type field
        default="jobseeker",  # Default value for user_type field
    )

    def __str__(self):
        """
        Returns a string representation of the user (username).
        """
        return self.username


class JobSeeker(models.Model):
    """
    Model representing a Job Seeker profile.
    """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True
    )  # One-to-one relationship with the User model
    bio = models.TextField(blank=True)  # Biography of the job seeker
    resume = models.FileField(
        upload_to="resumes/", blank=True
    )  # Resume file of the job seeker
    skills = models.CharField(
        max_length=200, blank=True
    )  # Skills of the job seeker

    def __str__(self):
        """
        Returns a string representation of the job seeker (username).
        """
        return self.user.username
