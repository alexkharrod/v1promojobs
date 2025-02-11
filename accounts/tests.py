from django.test import TestCase  # Import the TestCase class
from django.contrib.auth import get_user_model  # Import the get_user_model function
from .models import Employer, JobSeeker  # Import the Employer and JobSeeker models
from .forms import RegistrationForm  # Import the RegistrationForm

User = get_user_model()  # Get the User model

class UserManagementTests(TestCase):
    """
    Test class for user management functionalities.
    """
    def setUp(self):
        """
        Set up data for the tests.
        """
        self.username = 'testuser'  # Define a test username
        self.password = 'testpassword'  # Define a test password
        self.email = 'test@example.com'  # Define a test email

    def test_user_creation(self):
        """
        Test that a user can be created successfully.
        """
        user = User.objects.create_user(
            username=self.username, password=self.password, email=self.email
        )  # Create a new user
        self.assertEqual(user.username, self.username)  # Assert that the username is correct
        self.assertEqual(user.email, self.email)  # Assert that the email is correct
        self.assertTrue(
            user.check_password(self.password)
        )  # Assert that the password is correct

    def test_user_authentication(self):
        """
        Test that a user can be authenticated successfully.
        """
        user = User.objects.create_user(
            username=self.username, password=self.password, email=self.email
        )  # Create a new user
        authenticated_user = self.client.login(
            username=self.username, password=self.password
        )  # Log in the user
        self.assertTrue(authenticated_user)  # Assert that the user is authenticated

    def test_employer_profile_creation(self):
        """
        Test that an employer profile can be created successfully.
        """
        user = User.objects.create_user(
            username=self.username, password=self.password, email=self.email, user_type='employer'
        )  # Create a new employer user
        employer = Employer.objects.create(
            user=user, company_name='Test Company'
        )  # Create a new employer profile
        self.assertEqual(employer.user, user)  # Assert that the user is correct
        self.assertEqual(employer.company_name, 'Test Company')  # Assert that the company name is correct

    def test_jobseeker_profile_creation(self):
        """
        Test that a jobseeker profile can be created successfully.
        """
        user = User.objects.create_user(
            username=self.username, password=self.password, email=self.email, user_type='jobseeker'
        )  # Create a new job seeker user
        jobseeker = JobSeeker.objects.create(
            user=user, bio='Test Bio', skills='Test Skills'
        )  # Create a new job seeker profile
        self.assertEqual(jobseeker.user, user)  # Assert that the user is correct
        self.assertEqual(jobseeker.bio, 'Test Bio')  # Assert that the bio is correct
        self.assertEqual(jobseeker.skills, 'Test Skills')  # Assert that the skills are correct

    def test_registration_form_valid(self):
        """
        Test that the registration form is valid with valid data.
        """
        form_data = {
            'username': self.username,
            'password': self.password,
            'password2': self.password,
            'email': self.email,
            'user_type': 'jobseeker'
        }  # Create valid form data
        form = RegistrationForm(data=form_data)  # Create a RegistrationForm instance with the form data
        if not form.is_valid():  # Check if the form is valid
            print(form.errors)  # Print any form errors
        self.assertTrue(form.is_valid())  # Assert that the form is valid
        user = form.save(
            commit=False
        )  # Save the form data to create a new user (but don't commit to the database yet)
        user.set_password(self.password)  # Set the user's password
        user.save()  # Save the user to the database
        self.assertEqual(user.username, self.username)  # Assert that the username is correct
        self.assertEqual(user.email, self.email)  # Assert that the email is correct
        self.assertEqual(user.user_type, 'jobseeker')  # Assert that the user type is correct

    def test_registration_form_invalid(self):
        """
        Test that the registration form is invalid with invalid data.
        """
        form_data = {
            'username': self.username,
            'password': '',
            'email': self.email,
            'user_type': 'jobseeker'
        }  # Create invalid form data (empty password)
        form = RegistrationForm(data=form_data)  # Create a RegistrationForm instance with the form data
        self.assertFalse(form.is_valid())  # Assert that the form is invalid
