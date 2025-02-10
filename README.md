# v1promojobs

## Description

v1promojobs is a job board platform that connects employers with job seekers. It provides features for employers to post job listings and manage applications, and for job seekers to search for jobs and apply online.

## Features

*   User registration and authentication with dual user types (Employer/Job Seeker)
*   Profile management for both employers and job seekers
*   Job posting and management
*   Advanced search functionality with industry-specific filters
*   Job application management
*   Two-factor authentication

## Setup

1.  Clone the repository: `git clone [repository URL]`
2.  Create a virtual environment: `python -m venv .venv`
3.  Activate the virtual environment: `source .venv/bin/activate`
4.  Install dependencies: `pip install -r requirements.txt`
5.  Configure the database in `mysite/settings.py`
6.  Set up environment variables (especially `SECRET_KEY`) in `.env` file.
7.  Run migrations: `python manage.py migrate`
8.  Create a superuser: `python manage.py createsuperuser`
9.  Start the development server: `python manage.py runserver`

## Documentation

See the `docs` directory for architecture decision records (ADRs).

## License

[License information]
