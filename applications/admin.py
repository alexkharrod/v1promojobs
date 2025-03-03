from django.contrib import admin
from .models import Application

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'job_seeker', 'application_date', 'status')
    list_filter = ('status', 'application_date')
    search_fields = ('job__title', 'job_seeker__user__username')

admin.site.register(Application, ApplicationAdmin)
