from django.db import models  # Import the models module
from employers.models import Employer  # Import the Employer model

class Job(models.Model):
    """
    Model representing a job listing.
    """
    employer = models.ForeignKey(
        Employer, on_delete=models.CASCADE, help_text="Foreign key to the Employer model"
    )  # Foreign key to the Employer model
    title = models.CharField(
        max_length=200, help_text="Title of the job"
    )  # Title of the job
    description = models.TextField(help_text="Description of the job")  # Description of the job
    location = models.CharField(
        max_length=100, help_text="Location of the job"
    )  # Location of the job
    salary = models.CharField(max_length=50, help_text="Salary for the job")  # Salary for the job
    industry = models.CharField(
        max_length=100, blank=True, help_text="Industry of the job (optional)"
    )  # Industry of the job (optional)
    image = models.ImageField(
        upload_to="job_images/", blank=True, help_text="Image for the job (optional)"
    )  # Image for the job (optional)
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Date and time when the job was created"
    )  # Date and time when the job was created
    views = models.IntegerField(
        default=0, help_text="Number of views for the job"
    )  # Number of views for the job
    applications = models.IntegerField(
        default=0, help_text="Number of applications for the job"
    )  # Number of applications for the job

    def __str__(self):
        """
        Returns a string representation of the job (title).
        """
        return self.title


class SavedSearch(models.Model):
    """
    Model representing a saved search query.
    """
    user = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, help_text="Foreign key to the User model"
    )  # Foreign key to the User model
    query = models.CharField(
        max_length=200, blank=True, help_text="Search query (optional)"
    )  # Search query (optional)
    industry = models.CharField(
        max_length=100, blank=True, help_text="Industry for the search (optional)"
    )  # Industry for the search (optional)
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Date and time when the search was saved"
    )  # Date and time when the search was saved

    def __str__(self):
        """
        Returns a string representation of the saved search.
        """
        return f"Saved Search: {self.query} - {self.industry}"
