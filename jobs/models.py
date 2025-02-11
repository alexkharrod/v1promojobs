from django.db import models

from employers.models import Employer


class Job(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=100)
    salary = models.CharField(max_length=50)
    industry = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to="job_images/", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)

    views = models.IntegerField(default=0)
    applications = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class SavedSearch(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    query = models.CharField(max_length=200, blank=True)
    industry = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Saved Search: {self.query} - {self.industry}"
