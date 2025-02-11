from django.db import models
from jobs.models import Job  # Import the Job model from the jobs app
from accounts.models import JobSeeker  # Import the JobSeeker model from the accounts app

class Application(models.Model):
    """
    Model representing a job application.
    """
    job = models.ForeignKey(Job, on_delete=models.CASCADE)  # Foreign key to the Job model
    job_seeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE)  # Foreign key to the JobSeeker model
    application_date = models.DateTimeField(auto_now_add=True)  # Date and time when the application was submitted
    status = models.CharField(max_length=50, default='Pending')  # Status of the application (e.g., Pending, Accepted, Rejected)

    def __str__(self):
        """
        Returns a string representation of the application.
        """
        return f"Application for {self.job.title} by {self.job_seeker.user.username}"
