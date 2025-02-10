from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Application
from jobs.models import Job
from accounts.models import Employer, JobSeeker

User = get_user_model()

class ApplicationTests(TestCase):
    def setUp(self):
        # Set up data for the tests
        self.employer_username = 'testemployer'
        self.employer_password = 'testpassword'
        self.employer_email = 'testemployer@example.com'
        self.employer_user = User.objects.create_user(username=self.employer_username, password=self.employer_password, email=self.employer_email, user_type='employer')
        self.employer = Employer.objects.create(user=self.employer_user, company_name='Test Company')

        self.jobseeker_username = 'testjobseeker'
        self.jobseeker_password = 'testpassword'
        self.jobseeker_email = 'testjobseeker@example.com'
        self.jobseeker_user = User.objects.create_user(username=self.jobseeker_username, password=self.jobseeker_password, email=self.jobseeker_email, user_type='jobseeker')
        self.jobseeker = JobSeeker.objects.create(user=self.jobseeker_user)

        self.job = Job.objects.create(employer=self.employer, title='Test Job', description='Test Description', location='Test Location', salary='$100,000')

    def test_jobseeker_apply_for_job(self):
        # Test that a job seeker can apply for a job successfully
        self.client.login(username=self.jobseeker_username, password=self.jobseeker_password)
        response = self.client.get(f'/applications/apply/{self.job.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Application.objects.count(), 1)

    def test_employer_view_applications(self):
        # Test that an employer can view applications for a job successfully
        Application.objects.create(job=self.job, job_seeker=self.jobseeker)
        self.client.login(username=self.employer_username, password=self.employer_password)
        response = self.client.get(f'/applications/employer/{self.job.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['applications']), 1)

    def test_employer_update_application_status(self):
        # Test that an employer can update the status of an application successfully
        application = Application.objects.create(job=self.job, job_seeker=self.jobseeker)
        self.client.login(username=self.employer_username, password=self.employer_password)
        response = self.client.post(f'/applications/{application.id}/update_status/', {'status': 'Accepted'})
        self.assertEqual(response.status_code, 302)
        application.refresh_from_db()
        self.assertEqual(application.status, 'Accepted')
