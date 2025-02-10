from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Employer
from accounts.models import User

User = get_user_model()

class EmployerProfileTests(TestCase):
    def setUp(self):
        # Set up data for the tests
        self.username = 'testemployer'
        self.password = 'testpassword'
        self.email = 'testemployer@example.com'
        self.user = User.objects.create_user(username=self.username, password=self.password, email=self.email, user_type='employer')

    def test_employer_profile_creation(self):
        # Test that an employer profile can be created successfully
        employer = Employer.objects.create(user=self.user, company_name='Test Company', company_description='Test Description', website='https://www.example.com')
        self.assertEqual(employer.company_name, 'Test Company')
        self.assertEqual(employer.company_description, 'Test Description')
        self.assertEqual(employer.website, 'https://www.example.com')

    def test_employer_profile_editing(self):
        # Test that an employer profile can be edited successfully
        employer = Employer.objects.create(user=self.user, company_name='Test Company', company_description='Test Description', website='https://www.example.com')
        employer.company_name = 'Updated Test Company'
        employer.save()
        self.assertEqual(employer.company_name, 'Updated Test Company')

    def test_employer_profile_detail(self):
        # Test that an employer profile detail view returns the correct employer
        employer = Employer.objects.create(user=self.user, company_name='Test Company', company_description='Test Description', website='https://www.example.com')
        response = self.client.get(f'/employers/{employer.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['employer'], employer)
