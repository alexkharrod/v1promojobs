from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Job, SavedSearch
from accounts.models import Employer

User = get_user_model()

class JobManagementTests(TestCase):
    """
    Tests for the job management functionality.
    """
    def setUp(self):
        """
        Set up data for the tests.
        """
        self.username = 'testuser'  # Define a test username
        self.password = 'testpassword'  # Define a test password
        self.email = 'test@example.com'  # Define a test email
        self.user = User.objects.create_user(
            username=self.username, password=self.password, email=self.email, user_type='employer'
        )  # Create an employer user
        self.employer = Employer.objects.create(
            user=self.user, company_name='Test Company'
        )  # Create an employer profile

    def test_job_creation(self):
        """
        Test that a job can be created successfully.
        """
        job = Job.objects.create(
            employer=self.employer, title='Test Job', description='Test Description', location='Test Location', salary='$100,000'
        )  # Create a new job
        self.assertEqual(job.title, 'Test Job')  # Assert that the title is correct
        self.assertEqual(job.description, 'Test Description')  # Assert that the description is correct
        self.assertEqual(job.location, 'Test Location')  # Assert that the location is correct
        self.assertEqual(job.salary, '$100,000')  # Assert that the salary is correct

    def test_job_editing(self):
        """
        Test that a job can be edited successfully.
        """
        job = Job.objects.create(
            employer=self.employer, title='Test Job', description='Test Description', location='Test Location', salary='$100,000'
        )  # Create a new job
        job.title = 'Updated Test Job'  # Update the job title
        job.save()  # Save the updated job
        self.assertEqual(job.title, 'Updated Test Job')  # Assert that the title was updated

    def test_saved_search_creation(self):
        """
        Test that a saved search can be created successfully.
        """
        saved_search = SavedSearch.objects.create(
            user=self.user, query='Test Query', industry='Test Industry'
        )  # Create a new saved search
        self.assertEqual(saved_search.query, 'Test Query')  # Assert that the query is correct
        self.assertEqual(saved_search.industry, 'Test Industry')  # Assert that the industry is correct

    def test_saved_search_deletion(self):
        """
        Test that a saved search can be deleted successfully.
        """
        saved_search = SavedSearch.objects.create(
            user=self.user, query='Test Query', industry='Test Industry'
        )  # Create a new saved search
        saved_search.delete()  # Delete the saved search
        self.assertEqual(SavedSearch.objects.count(), 0)  # Assert that the saved search was deleted
