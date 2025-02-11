from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class SavedSearch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='search_saved_searches')
    query = models.CharField(max_length=255, blank=True)
    industry = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Saved Search: {self.query} - {self.industry}"
