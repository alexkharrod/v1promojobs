from django.db import models  # Import the models module
from accounts.models import User  # Import the User model

class Employer(models.Model):
    """
    Model representing an Employer profile.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='employer_profile',
        help_text="One-to-one relationship with the User model"
    )  # One-to-one relationship with the User model
    company_name = models.CharField(
        max_length=200,
        help_text="Name of the company"
    )  # Name of the company
    company_description = models.TextField(
        blank=True,
        help_text="Description of the company"
    )  # Description of the company
    website = models.URLField(
        blank=True,
        help_text="Website URL of the company"
    )  # Website URL of the company
    logo = models.ImageField(
        upload_to='employer_logos/', blank=True,
        help_text="Logo of the company"
    )  # Logo of the company

    def __str__(self):
        """
        Returns a string representation of the employer (company name).
        """
        return self.company_name
