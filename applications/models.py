from django.db import models
from jobs.models import Job
from accounts.models import JobSeeker

class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    job_seeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE)
    application_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Pending')

    def __str__(self):
        return f"Application for {self.job.title} by {self.job_seeker.user.username}"
