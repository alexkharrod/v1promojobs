from django.db import models  # Import the models module
from django.contrib.auth import get_user_model  # Import the get_user_model function

User = get_user_model()  # Get the User model

class SavedSearch(models.Model):
    """
    Model representing a saved search query.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='search_saved_searches',
        help_text="Foreign key to the User model"
    )  # Foreign key to the User model
    query = models.CharField(
        max_length=255,
        blank=True,
        help_text="Search query (optional)"
    )  # The saved search query
    industry = models.CharField(
        max_length=255,
        blank=True,
        help_text="Industry for the search (optional)"
    )  # The saved search industry
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time when the search was saved"
    )  # The date and time the search was saved

    def __str__(self):
        """
        Returns a string representation of the saved search.
        """
        return f"Saved Search: {self.query} - {self.industry}"
