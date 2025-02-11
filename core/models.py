from django.db import models  # Import the models module
from django.contrib.auth import get_user_model  # Import the get_user_model function

User = get_user_model()  # Get the User model

class UserActivity(models.Model):
    """
    Model representing user activity for analytics.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="Foreign key to the User model",
    )  # Foreign key to the User model
    activity_type = models.CharField(
        max_length=255,
        help_text="Type of user activity (e.g., login, job_search)"
    )  # Type of user activity (e.g., login, job_search, profile_view)
    timestamp = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time of the activity"
    )  # Date and time of the activity
    details = models.JSONField(
        blank=True, null=True,
        help_text="Additional details about the activity"
    )  # Additional details about the activity (e.g., search query)

    def __str__(self):
        """
        Returns a string representation of the user activity.
        """
        return f"{self.user.username} - {self.activity_type} - {self.timestamp}"
