from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Employer, JobSeeker
from .forms import RegistrationForm

User = get_user_model()

class UserManagementTests(TestCase):
    def setUp(self):
        # Set up data for the tests
        self.username = 'testuser'
        self.password = 'testpassword'
        self.email = 'test@example.com'

    def test_user_creation(self):
        # Test that a user can be created successfully
        user = User.objects.create_user(username=self.username, password=self.password, email=self.email)
        self.assertEqual(user.username, self.username)
        self.assertEqual(user.email, self.email)
        self.assertTrue(user.check_password(self.password))

    def test_user_authentication(self):
        # Test that a user can be authenticated successfully
        user = User.objects.create_user(username=self.username, password=self.password, email=self.email)
        authenticated_user = self.client.login(username=self.username, password=self.password)
        self.assertTrue(authenticated_user)

    def test_employer_profile_creation(self):
        # Test that an employer profile can be created successfully
        user = User.objects.create_user(username=self.username, password=self.password, email=self.email, user_type='employer')
        employer = Employer.objects.create(user=user, company_name='Test Company')
        self.assertEqual(employer.user, user)
        self.assertEqual(employer.company_name, 'Test Company')

    def test_jobseeker_profile_creation(self):
        # Test that a jobseeker profile can be created successfully
        user = User.objects.create_user(username=self.username, password=self.password, email=self.email, user_type='jobseeker')
        jobseeker = JobSeeker.objects.create(user=user, bio='Test Bio', skills='Test Skills')
        self.assertEqual(jobseeker.user, user)
        self.assertEqual(jobseeker.bio, 'Test Bio')
        self.assertEqual(jobseeker.skills, 'Test Skills')

    def test_registration_form_valid(self):
        # Test that the registration form is valid with valid data
        form_data = {'username': self.username, 'password': self.password, 'password2': self.password, 'email': self.email, 'user_type': 'jobseeker'}
    def test_registration_form_valid(self):
        # Test that the registration form is valid with valid data
        form_data = {'username': self.username, 'password1': self.password, 'password2': self.password, 'email': self.email, 'user_type': 'jobseeker'}
        form = RegistrationForm(data=form_data)
        if not form.is_valid():
            print(form.errors)
        self.assertTrue(form.is_valid())
        user = form.save(commit=False)
        user.set_password(self.password)
        user.save()
        self.assertEqual(user.username, self.username)
        self.assertEqual(user.email, self.email)
        self.assertEqual(user.user_type, 'jobseeker')

    def test_registration_form_invalid(self):
        # Test that the registration form is invalid with invalid data
        form_data = {'username': self.username, 'password': '', 'email': self.email, 'user_type': 'jobseeker'}
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
