from django.test import TestCase
from django.contrib.auth import get_user_model
from jobs.models import Job
from .models import SavedSearch
from .forms import SearchForm
from employers.models import Employer

User = get_user_model()

class SearchTests(TestCase):
    def setUp(self):
        # Set up data for the tests
        self.username = 'testuser'
        self.password = 'testpassword'
        self.email = 'test@example.com'
        self.user = User.objects.create_user(username=self.username, password=self.password, email=self.email, user_type='employer')
        self.employer = Employer.objects.create(user=self.user, company_name='Test Company')

        self.job1 = Job.objects.create(employer=self.employer, title='Test Job 1', description='Test Description', location='Test Location', salary='$100,000', industry='Technology')
        self.job2 = Job.objects.create(employer=self.employer, title='Test Job 2', description='Test Description', location='Test Location', salary='$100,000', industry='Healthcare')

    def test_search_functionality(self):
        # Test that the search functionality returns the correct results
        response = self.client.get('/search/', {'query': 'Test Job', 'industry': 'Technology'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['jobs']), 1)
        self.assertEqual(response.context['jobs'][0].title, 'Test Job 1')

    def test_saved_search_creation(self):
        # Test that a saved search can be created successfully
        self.client.login(username=self.username, password=self.password)
        response = self.client.post('/search/save_search/', {'query': 'Test Job', 'industry': 'Technology'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(SavedSearch.objects.count(), 1)

    def test_saved_search_deletion(self):
        # Test that a saved search can be deleted successfully
        self.client.login(username=self.username, password=self.password)
        saved_search = SavedSearch.objects.create(user=self.user, query='Test Query', industry='Test Industry')
        response = self.client.get(f'/search/delete_saved_search/{saved_search.pk}/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(SavedSearch.objects.count(), 0)
