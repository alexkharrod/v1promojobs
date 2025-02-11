from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Employer
from accounts.models import User

User = get_user_model()

class EmployerProfileTests(TestCase):
    """
    Tests for the employer profile functionality.
    """
    def setUp(self):
        """
        Set up data for the tests.
        """
        self.username = 'testemployer'  # Define a test username
        self.password = 'testpassword'  # Define a test password
        self.email = 'testemployer@example.com'  # Define a test email
        self.user = User.objects.create_user(
            username=self.username, password=self.password, email=self.email, user_type='employer'
        )  # Create an employer user

    def test_employer_profile_creation(self):
        """
        Test that an employer profile can be created successfully.
        """
        employer = Employer.objects.create(
            user=self.user, company_name='Test Company', company_description='Test Description', website='https://www.example.com'
        )  # Create a new employer profile
        self.assertEqual(employer.company_name, 'Test Company')  # Assert that the company name is correct
        self.assertEqual(employer.company_description, 'Test Description')  # Assert that the company description is correct
        self.assertEqual(employer.website, 'https://www.example.com')  # Assert that the website is correct

    def test_employer_profile_editing(self):
        """
        Test that an employer profile can be edited successfully.
        """
        employer = Employer.objects.create(
            user=self.user, company_name='Test Company', company_description='Test Description', website='https://www.example.com'
        )  # Create a new employer profile
        employer.company_name = 'Updated Test Company'  # Update the company name
        employer.save()  # Save the updated employer profile
        self.assertEqual(employer.company_name, 'Updated Test Company')  # Assert that the company name was updated

    def test_employer_profile_detail(self):
        """
        Test that an employer profile detail view returns the correct employer.
        """
        employer = Employer.objects.create(
            user=self.user, company_name='Test Company', company_description='Test Description', website='https://www.example.com'
        )  # Create a new employer profile
        response = self.client.get(
            f'/employers/{employer.pk}/'
        )  # Get the employer profile detail view
        self.assertEqual(response.status_code, 200)  # Assert that the response status code is 200 OK
        self.assertEqual(response.context['employer'], employer)  # Assert that the employer object is in the context
