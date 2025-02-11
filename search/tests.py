from django.test import TestCase
from django.contrib.auth import get_user_model
from jobs.models import Job
from .models import SavedSearch
from .forms import SearchForm
from employers.models import Employer

User = get_user_model()

class SearchTests(TestCase):
    """
    Tests for the search functionality.
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

        self.job1 = Job.objects.create(
            employer=self.employer, title='Test Job 1', description='Test Description', location='Test Location', salary='$100,000', industry='Technology'
        )  # Create a job listing
        self.job2 = Job.objects.create(
            employer=self.employer, title='Test Job 2', description='Test Description', location='Test Location', salary='$100,000', industry='Healthcare'
        )  # Create another job listing

    def test_search_functionality(self):
        """
        Test that the search functionality returns the correct results.
        """
        response = self.client.get(
            '/search/', {'query': 'Test Job', 'industry': 'Technology'}
        )  # Perform a search
        self.assertEqual(response.status_code, 200)  # Assert that the response status code is 200 OK
        self.assertEqual(len(response.context['jobs']), 1)  # Assert that one job is returned
        self.assertEqual(response.context['jobs'][0].title, 'Test Job 1')  # Assert that the correct job is returned

    def test_saved_search_creation(self):
        """
        Test that a saved search can be created successfully.
        """
        self.client.login(username=self.username, password=self.password)  # Log in as the user
        response = self.client.post(
            '/search/save_search/', {'query': 'Test Job', 'industry': 'Technology'}
        )  # Save the search
        self.assertEqual(response.status_code, 302)  # Assert that the response status code is 302 (redirect)
        self.assertEqual(SavedSearch.objects.count(), 1)  # Assert that a saved search was created

    def test_saved_search_deletion(self):
        """
        Test that a saved search can be deleted successfully.
        """
        self.client.login(username=self.username, password=self.password)  # Log in as the user
        saved_search = SavedSearch.objects.create(
            user=self.user, query='Test Query', industry='Test Industry'
        )  # Create a new saved search
        response = self.client.get(
            f'/search/delete_saved_search/{saved_search.pk}/'
        )  # Delete the saved search
        self.assertEqual(response.status_code, 302)  # Assert that the response status code is 302 (redirect)
        self.assertEqual(SavedSearch.objects.count(), 0)  # Assert that the saved search was deleted
