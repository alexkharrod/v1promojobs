from django.test import TestCase  # Import the TestCase class
from django.contrib.auth import get_user_model  # Import the get_user_model function
from .models import Application  # Import the Application model
from jobs.models import Job  # Import the Job model
from accounts.models import Employer, JobSeeker  # Import the Employer and JobSeeker models
from .forms import ApplicationForm  # Import the ApplicationForm

User = get_user_model()  # Get the User model

class ApplicationTests(TestCase):
    """
    Tests for the application management functionality.
    """
    def setUp(self):
        """
        Set up data for the tests.
        """
        self.employer_username = 'testemployer'  # Username for the employer user
        self.employer_password = 'testpassword'  # Password for the employer user
        self.employer_email = 'testemployer@example.com'  # Email for the employer user
        self.employer_user = User.objects.create_user(username=self.employer_username, password=self.employer_password, email=self.employer_email, user_type='employer')  # Create an employer user
        self.employer = Employer.objects.create(user=self.employer_user, company_name='Test Company')  # Create an employer profile

        self.jobseeker_username = 'testjobseeker'  # Username for the job seeker user
        self.jobseeker_password = 'testpassword'  # Password for the job seeker user
        self.jobseeker_email = 'testjobseeker@example.com'  # Email for the job seeker user
        self.jobseeker_user = User.objects.create_user(username=self.jobseeker_username, password=self.jobseeker_password, email=self.jobseeker_email, user_type='jobseeker')  # Create a job seeker user
        self.jobseeker = JobSeeker.objects.create(user=self.jobseeker_user)  # Create a job seeker profile

        self.job = Job.objects.create(employer=self.employer, title='Test Job', description='Test Description', location='Test Location', salary='$100,000')  # Create a job listing

    def test_jobseeker_apply_for_job(self):
        """
        Test that a job seeker can apply for a job successfully.
        """
        self.client.login(username=self.jobseeker_username, password=self.jobseeker_password)  # Log in as the job seeker
        response = self.client.get(f'/applications/apply/{self.job.id}/')  # Apply for the job
        self.assertEqual(response.status_code, 302)  # Expect a redirect
        self.assertEqual(Application.objects.count(), 1)  # Check that an application was created

    def test_employer_view_applications(self):
        """
        Test that an employer can view applications for a job successfully.
        """
        Application.objects.create(job=self.job, job_seeker=self.jobseeker)  # Create an application
        self.client.login(username=self.employer_username, password=self.employer_password)  # Log in as the employer
        response = self.client.get(f'/applications/employer/{self.job.id}/')  # View the applications for the job
        self.assertEqual(response.status_code, 200)  # Expect a 200 OK
        self.assertEqual(len(response.context['applications']), 1)  # Check that the application is in the context

    def test_employer_update_application_status(self):
        """
        Test that an employer can update the status of an application successfully.
        """
        application = Application.objects.create(job=self.job, job_seeker=self.jobseeker)  # Create an application
        self.client.login(username=self.employer_username, password=self.employer_password)  # Log in as the employer
        response = self.client.post(f'/applications/{application.id}/update_status/', {'status': 'Accepted'})  # Update the application status
        self.assertEqual(response.status_code, 302)  # Expect a redirect
        application.refresh_from_db()  # Refresh the application from the database
        self.assertEqual(application.status, 'Accepted')  # Check that the status was updated
