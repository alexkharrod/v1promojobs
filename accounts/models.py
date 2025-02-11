from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ("employer", "Employer"),
        ("jobseeker", "Job Seeker"),
    )
    user_type = models.CharField(
        max_length=10, choices=USER_TYPE_CHOICES, default="jobseeker"
    )

    def __str__(self):
        return self.username


class JobSeeker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    bio = models.TextField(blank=True)
    resume = models.FileField(upload_to="resumes/", blank=True)
    skills = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.user.username
