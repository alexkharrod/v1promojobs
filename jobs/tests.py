from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Job, SavedSearch
from accounts.models import Employer

User = get_user_model()

class JobManagementTests(TestCase):
    def setUp(self):
        # Set up data for the tests
        self.username = 'testuser'
        self.password = 'testpassword'
        self.email = 'test@example.com'
        self.user = User.objects.create_user(username=self.username, password=self.password, email=self.email, user_type='employer')
        self.employer = Employer.objects.create(user=self.user, company_name='Test Company')

    def test_job_creation(self):
        # Test that a job can be created successfully
        job = Job.objects.create(employer=self.employer, title='Test Job', description='Test Description', location='Test Location', salary='$100,000')
        self.assertEqual(job.title, 'Test Job')
        self.assertEqual(job.description, 'Test Description')
        self.assertEqual(job.location, 'Test Location')
        self.assertEqual(job.salary, '$100,000')

    def test_job_editing(self):
        # Test that a job can be edited successfully
        job = Job.objects.create(employer=self.employer, title='Test Job', description='Test Description', location='Test Location', salary='$100,000')
        job.title = 'Updated Test Job'
        job.save()
        self.assertEqual(job.title, 'Updated Test Job')

    def test_saved_search_creation(self):
        # Test that a saved search can be created successfully
        saved_search = SavedSearch.objects.create(user=self.user, query='Test Query', industry='Test Industry')
        self.assertEqual(saved_search.query, 'Test Query')
        self.assertEqual(saved_search.industry, 'Test Industry')

    def test_saved_search_deletion(self):
        # Test that a saved search can be deleted successfully
        saved_search = SavedSearch.objects.create(user=self.user, query='Test Query', industry='Test Industry')
        saved_search.delete()
        self.assertEqual(SavedSearch.objects.count(), 0)
