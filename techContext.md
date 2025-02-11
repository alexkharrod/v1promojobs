# Technical Context

## Technology Stack

### Backend Framework
- Python 3.12
- Django 4.2
- Django REST Framework
- SQLite Database
- Redis Cache

### Frontend Technologies
- Django Templates
- HTML5
- CSS3
- JavaScript
- React/Vue.js (for interactive components)

### Development Environment
- Virtual Environment: .venv
- IDE Support: VS Code recommended
- Git for version control
- Docker for containerization

## Development Setup

### Prerequisites
```bash
# Python 3.12
# pip
# virtualenv
# git
# redis-server
```

### Environment Setup
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows
.venv\Scripts\activate
# Unix/MacOS
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Project Structure
```
project_root/
├── .venv/
├── .env                    # Environment variables (git-ignored)
├── cline_docs/            # Memory bank documentation
├── docs/                  # Project documentation
│   ├── adr/              # Architecture Decision Records
│   └── api/              # API documentation
├── src/
│   ├── accounts/         # User management
│   ├── jobs/            # Job listings
│   ├── employers/       # Employer profiles
│   ├── applications/    # Job applications
│   ├── search/          # Search functionality
│   └── core/            # Core functionality
├── static/              # Static files
│   ├── css/
│   ├── js/
│   └── images/
└── templates/           # HTML templates
```

## Technical Constraints

### Performance Requirements
- Page load time < 3 seconds
- Search response time < 1 second
- File upload size limits: 10MB max

### Browser Support
- Modern browsers (last 2 versions)
- Mobile-responsive design required

### Security Requirements
- HTTPS required (using Let's Encrypt)
- SQL injection prevention
- XSS protection
- CSRF protection
- Rate limiting implementation

## Rate Limiting

Rate limiting is used to protect the API and website from abuse by limiting the number of requests that a user can make within a certain time period.

### Implementation Details

This project uses the `django-ratelimit` package for rate limiting.

1.  **Middleware:**

    The `RatelimitMiddleware` is used for global rate limiting. It applies rate limits to all views in the project.

    To enable the middleware, add it to the `MIDDLEWARE` setting in `mysite/settings.py`:

    ```python
    MIDDLEWARE = [
        ...,
        'django_ratelimit.middleware.RatelimitMiddleware',
    ]
    ```

2.  **`ratelimit` Decorator:**

    The `ratelimit` decorator is used for view-specific rate limiting. It allows you to apply rate limits to individual views.

    ```python
    from django_ratelimit.decorators import ratelimit

    @ratelimit(key='ip', rate='5/m', method='GET')
    def my_view(request):
        was_limited = getattr(request, 'limited', False)
        if was_limited:
            return HttpResponse('Rate limited!')
        else:
            return HttpResponse('Hello!')
    ```

    *   `key`: Specifies the key to use for rate limiting (e.g., 'ip' for IP address, 'user' for user ID).
    *   `rate`: Specifies the rate limit (e.g., '5/m' for 5 requests per minute).
    *   `method`: Specifies the HTTP methods to apply the rate limit to (e.g., 'GET', 'POST').

3.  **Configuration Options:**

    The following configuration options are available in `mysite/settings.py`:

    *   `RATELIMIT_USE_XFORWARDEDFOR`: Set to `True` if your server is behind a proxy.
    *   `RATELIMIT_DEFAULT_RATE`: Specifies the default rate limit for all views.

### Important Considerations

*   Choose appropriate rate limits to balance security and usability.
*   Monitor rate limiting activity to identify potential attacks.
*   Consider using different rate limits for different types of users or API endpoints.
# Technical Context

## Technology Stack

### Backend Framework
- Python 3.12
- Django 4.2
- Django REST Framework
- SQLite Database
- Redis Cache

### Frontend Technologies
- Django Templates
- HTML5
- CSS3
- JavaScript
- React/Vue.js (for interactive components)

### Development Environment
- Virtual Environment: .venv
- IDE Support: VS Code recommended
- Git for version control
- Docker for containerization

## Development Setup

### Prerequisites
```bash
# Python 3.12
# pip
# virtualenv
# git
# redis-server
```

### Environment Setup
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows
.venv\Scripts\activate
# Unix/MacOS
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Project Structure
```
project_root/
├── .venv/
├── .env                    # Environment variables (git-ignored)
├── cline_docs/            # Memory bank documentation
├── docs/                  # Project documentation
│   ├── adr/              # Architecture Decision Records
│   └── api/              # API documentation
├── src/
│   ├── accounts/         # User management
│   ├── jobs/            # Job listings
│   ├── employers/       # Employer profiles
│   ├── applications/    # Job applications
│   ├── search/          # Search functionality
│   └── core/            # Core functionality
├── static/              # Static files
│   ├── css/
│   ├── js/
│   └── images/
└── templates/           # HTML templates
```

## Technical Constraints

### Performance Requirements
- Page load time < 3 seconds
- Search response time < 1 second
- File upload size limits: 10MB max

### Browser Support
- Modern browsers (last 2 versions)
- Mobile-responsive design required

### Security Requirements
- HTTPS required (using Let's Encrypt)
- SQL injection prevention
- XSS protection
- CSRF protection
- Rate limiting implementation

## XSS (Cross-Site Scripting) Protection

Cross-Site Scripting (XSS) attacks occur when malicious scripts are injected into trusted websites. Django provides several built-in mechanisms to prevent XSS attacks.

### Best Practices in Django

1.  **Automatic HTML Escaping in Templates:**

    Django's template engine automatically escapes HTML, which means that it converts potentially dangerous characters into their HTML entity equivalents. This prevents browsers from interpreting them as code.

    ```html
    {# Example of automatic HTML escaping #}
    {{ user.name }}
    ```

2.  **Validate and Sanitize User Input:**

    Always validate and sanitize user input to prevent malicious data from being injected into your templates. Use Django's built-in form validation and sanitization tools.

    ```python
    from django import forms
    from django.utils.html import escape

    class CommentForm(forms.Form):
        text = forms.CharField(max_length=200)

        def clean_text(self):
            text = self.cleaned_data['text']
            return escape(text)

    def comment_view(request):
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                text = form.cleaned_data['text']
                # Save the comment
            else:
                # Handle invalid form data
        else:
            form = CommentForm()
        return render(request, 'comment.html', {'form': form})
    ```

3.  **Use the `safe` Filter Sparingly:**

    The `safe` filter tells Django that a variable contains safe HTML that doesn't need to be escaped. Use this filter sparingly and only when you are absolutely sure that the content is safe.

    ```html
    {# Example of using the safe filter #}
    {{ trusted_html|safe }}
    ```

4.  **Set the `X-Content-Type-Options` Header:**

    Setting the `X-Content-Type-Options` header to `nosniff` prevents browsers from trying to MIME-sniff the content type of a response. This can help prevent XSS attacks that exploit MIME-sniffing vulnerabilities.

    You can set this header in your Django settings:

    ```python
    SECURE_HSTS_SECONDS = 31536000
    SECURE_CONTENT_TYPE_NOSNIFF = True
    ```

5.  **Use a Content Security Policy (CSP):**

    A Content Security Policy (CSP) is an HTTP header that allows you to control the resources that the browser is allowed to load for a given page. This can help prevent XSS attacks by restricting the sources from which scripts can be loaded.

    You can configure CSP in your Django settings using a package like `django-csp`:

    ```python
    # Install django-csp
    pip install django-csp

    # Add it to INSTALLED_APPS
    INSTALLED_APPS = [
        ...,
        'csp',
    ]

    # Configure CSP settings
    CSP_DEFAULT_SRC = ("'self'",)
    CSP_SCRIPT_SRC = ("'self'", "https://unpkg.com")
    CSP_STYLE_SRC = ("'self'", "https://cdn.jsdelivr.net")
    CSP_IMG_SRC = ("'self'",)
    ```

By following these best practices, you can significantly reduce the risk of XSS attacks in your Django project.
# Technical Context

## Technology Stack

### Backend Framework
- Python 3.12
- Django 4.2
- Django REST Framework
- SQLite Database
- Redis Cache

### Frontend Technologies
- Django Templates
- HTML5
- CSS3
- JavaScript
- React/Vue.js (for interactive components)

### Development Environment
- Virtual Environment: .venv
- IDE Support: VS Code recommended
- Git for version control
- Docker for containerization

## Development Setup

### Prerequisites
```bash
# Python 3.12
# pip
# virtualenv
# git
# redis-server
```

### Environment Setup
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows
.venv\Scripts\activate
# Unix/MacOS
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Project Structure
```
project_root/
├── .venv/
├── .env                    # Environment variables (git-ignored)
├── cline_docs/            # Memory bank documentation
├── docs/                  # Project documentation
│   ├── adr/              # Architecture Decision Records
│   └── api/              # API documentation
├── src/
│   ├── accounts/         # User management
│   ├── jobs/            # Job listings
│   ├── employers/       # Employer profiles
│   ├── applications/    # Job applications
│   ├── search/          # Search functionality
│   └── core/            # Core functionality
├── static/              # Static files
│   ├── css/
│   ├── js/
│   └── images/
└── templates/           # HTML templates
```

## Technical Constraints

### Performance Requirements
- Page load time < 3 seconds
- Search response time < 1 second
- File upload size limits: 10MB max

### Browser Support
- Modern browsers (last 2 versions)
- Mobile-responsive design required

### Security Requirements
- HTTPS required (using Let's Encrypt)
- SQL injection prevention
- XSS protection
- CSRF protection
- Rate limiting implementation

## SQL Injection Prevention

SQL injection is a code injection technique that might allow an attacker to execute malicious SQL statements that could control a database server.

### Best Practices in Django

1.  **Use Django's ORM:**

    Django's ORM (Object-Relational Mapper) provides a high-level interface for interacting with databases. It automatically escapes queries, which significantly reduces the risk of SQL injection.

    ```python
    # Example using Django's ORM
    from .models import Job

    jobs = Job.objects.filter(title__contains='Python')
    ```

2.  **Avoid Raw SQL Queries:**

    Whenever possible, avoid using raw SQL queries. Raw SQL queries bypass the ORM's built-in protection mechanisms.

3.  **Use Parameterized Queries with Proper Escaping:**

    If you must use raw SQL queries, use parameterized queries with proper escaping. This ensures that user-provided data is treated as data, not as code.

    ```python
    from django.db import connection

    def get_jobs_by_title(title):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM jobs_job WHERE title LIKE %s", [title])
            rows = cursor.fetchall()
        return rows
    ```

4.  **Validate and Sanitize User Input:**

    Always validate and sanitize user input to prevent malicious data from being injected into your queries. Use Django's built-in form validation and sanitization tools.

    ```python
    from django import forms

    class SearchForm(forms.Form):
        title = forms.CharField(max_length=100)

    def search_view(request):
        if request.method == 'POST':
            form = SearchForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                # Use the title in a query
            else:
                # Handle invalid form data
        else:
            form = SearchForm()
        return render(request, 'search.html', {'form': form})
    ```

By following these best practices, you can significantly reduce the risk of SQL injection in your Django project.
# Technical Context

## Technology Stack

### Backend Framework
- Python 3.12
- Django 4.2
- Django REST Framework
- SQLite Database
- Redis Cache

### Frontend Technologies
- Django Templates
- HTML5
- CSS3
- JavaScript
- React/Vue.js (for interactive components)

### Development Environment
- Virtual Environment: .venv
- IDE Support: VS Code recommended
- Git for version control
- Docker for containerization

## Development Setup

### Prerequisites
```bash
# Python 3.12
# pip
# virtualenv
# git
# redis-server
```

### Environment Setup
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows
.venv\Scripts\activate
# Unix/MacOS
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Project Structure
```
project_root/
├── .venv/
├── .env                    # Environment variables (git-ignored)
├── cline_docs/            # Memory bank documentation
├── docs/                  # Project documentation
│   ├── adr/              # Architecture Decision Records
│   └── api/              # API documentation
├── src/
│   ├── accounts/         # User management
│   ├── jobs/            # Job listings
│   ├── employers/       # Employer profiles
│   ├── applications/    # Job applications
│   ├── search/          # Search functionality
│   └── core/            # Core functionality
├── static/              # Static files
│   ├── css/
│   ├── js/
│   └── images/
└── templates/           # HTML templates
```

## Technical Constraints

### Performance Requirements
- Page load time < 3 seconds
- Search response time < 1 second
- File upload size limits: 10MB max

### Browser Support
- Modern browsers (last 2 versions)
- Mobile-responsive design required

### Security Requirements
- HTTPS required (using Let's Encrypt)
- SQL injection prevention
- XSS protection
- CSRF protection
- Rate limiting implementation

## HTTPS Implementation

To implement HTTPS, you will need to:

1.  Obtain an SSL/TLS certificate from a certificate authority like Let's Encrypt.
2.  Configure your web server (e.g., Nginx or Apache) to use the certificate.

Here's a general outline of the steps involved:

### Using Let's Encrypt with Certbot

Let's Encrypt is a free, automated, and open certificate authority. You can use Certbot, a tool that automates the process of obtaining and installing Let's Encrypt certificates.

1.  **Install Certbot:**

    ```bash
    # For Debian/Ubuntu:
    sudo apt update
    sudo apt install certbot

    # For CentOS/RHEL:
    sudo yum install epel-release
    sudo yum install certbot

    # For macOS:
    brew install certbot
    ```

2.  **Obtain a Certificate:**

    *   **For Nginx:**

        ```bash
        sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
        ```

    *   **For Apache:**

        ```bash
        sudo certbot --apache -d yourdomain.com -d www.yourdomain.com
        ```

    Replace `yourdomain.com` with your actual domain name.

3.  **Certbot will guide you through the process of configuring your web server to use the certificate.**

4.  **Automatic Renewal:**

    Certbot also sets up automatic renewal of your certificates. You can test the renewal process with:

    ```bash
    sudo certbot renew --dry-run
    ```

### Manual Configuration

If you prefer to configure HTTPS manually, you'll need to:

1.  Obtain an SSL/TLS certificate from a certificate authority.
2.  Configure your web server to point to the certificate and private key files.
3.  Ensure that your web server is listening on port 443 (the standard port for HTTPS).

### Important Considerations

*   Always use strong SSL/TLS configurations.
*   Keep your certificates up to date.
*   Regularly test your HTTPS configuration using tools like SSL Labs' SSL Server Test.
# Technical Context

## Technology Stack

### Backend Framework
- Python 3.12
- Django 4.2
- Django REST Framework
- SQLite Database
- Redis Cache

### Frontend Technologies
- Django Templates
- HTML5
- CSS3
- JavaScript
- React/Vue.js (for interactive components)

### Development Environment
- Virtual Environment: .venv
- IDE Support: VS Code recommended
- Git for version control
- Docker for containerization

## Development Setup

### Prerequisites
```bash
# Python 3.12
# pip
# virtualenv
# git
# redis-server
```

### Environment Setup
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows
.venv\Scripts\activate
# Unix/MacOS
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Project Structure
```
project_root/
├── .venv/
├── .env                    # Environment variables (git-ignored)
├── cline_docs/            # Memory bank documentation
├── docs/                  # Project documentation
│   ├── adr/              # Architecture Decision Records
│   └── api/              # API documentation
├── src/
│   ├── accounts/         # User management
│   ├── jobs/            # Job listings
│   ├── employers/       # Employer profiles
│   ├── applications/    # Job applications
│   ├── search/          # Search functionality
│   └── core/            # Core functionality
├── static/              # Static files
│   ├── css/
│   ├── js/
│   └── images/
└── templates/           # HTML templates
```

## Technical Constraints

### Performance Requirements
- Page load time < 3 seconds
- Search response time < 1 second
- File upload size limits: 10MB max

### Browser Support
- Modern browsers (last 2 versions)
- Mobile-responsive design required

### Security Requirements
- HTTPS required
- SQL injection prevention
- XSS protection
- CSRF protection
- Rate limiting implementation

## Integration Points

### External Services
- Email service integration
- File storage service
- Payment processing (future)
- Analytics integration

### API Architecture
- RESTful API design
- JSON response format
- Token-based authentication
- Rate limiting implementation

## Monitoring and Logging

### Application Monitoring
- Error tracking
- Performance monitoring
- User activity logging

### Security Monitoring
- Authentication attempts
- Authorization failures
- Resource access logging

## Deployment Considerations

### Environment Configuration
- Development
- Staging
- Production

### Database Management
- Migration strategy
- Backup procedures
- Data retention policies

## Documentation Requirements

### Code Documentation
- Docstrings required
- README files
- API documentation
- Architectural documentation

### Testing Documentation
- Test cases
- Testing procedures
- Coverage reports
