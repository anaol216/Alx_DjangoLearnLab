# Security Implementation Documentation

This document details all security measures implemented in the LibraryProject Django application to protect against common web vulnerabilities.

## Table of Contents

1. [Security Settings Configuration](#security-settings-configuration)
2. [CSRF Protection](#csrf-protection)
3. [XSS Protection](#xss-protection)
4. [SQL Injection Prevention](#sql-injection-prevention)
5. [Content Security Policy (CSP)](#content-security-policy)
6. [Session Security](#session-security)
7. [Input Validation and Sanitization](#input-validation-and-sanitization)
8. [Production Deployment Checklist](#production-deployment-checklist)

---

## Security Settings Configuration

### Location: `LibraryProject/settings.py`

### Key Security Settings:

#### 1. DEBUG Mode
```python
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
```
- **Purpose**: Prevents exposing sensitive error information in production
- **Security Impact**: When `DEBUG=False`, Django hides stack traces and database queries from error pages
- **Production**: Always set `DEBUG=False` in production

#### 2. ALLOWED_HOSTS
```python
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',') if os.environ.get('ALLOWED_HOSTS') else ['localhost', '127.0.0.1']
```
- **Purpose**: Prevents HTTP Host header attacks
- **Security Impact**: Only allows requests from specified domains
- **Production**: Set to your actual domain names

#### 3. SECRET_KEY
```python
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-...')
```
- **Purpose**: Used for cryptographic signing (sessions, CSRF tokens, etc.)
- **Security Impact**: Must be kept secret and unique
- **Production**: Use environment variable, never commit to version control

---

## CSRF Protection

### Implementation

#### 1. Middleware
```python
'django.middleware.csrf.CsrfViewMiddleware'
```
- Automatically enabled in `MIDDLEWARE`
- Validates CSRF tokens on all POST requests

#### 2. Settings
```python
CSRF_COOKIE_SECURE = not DEBUG  # True in production
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'
```
- **CSRF_COOKIE_SECURE**: Ensures cookies only sent over HTTPS
- **CSRF_COOKIE_HTTPONLY**: Prevents JavaScript access
- **CSRF_COOKIE_SAMESITE**: Controls when cookie is sent

#### 3. Templates
All POST forms include:
```django
{% csrf_token %}
```

#### 4. Views
Views that handle POST requests use:
```python
@csrf_protect
def my_view(request):
    # View code
```

### How It Works

1. Django generates a unique CSRF token per session
2. Token is included in forms via `{% csrf_token %}`
3. On POST, Django validates the token matches the session
4. Invalid tokens result in 403 Forbidden error

### Testing CSRF Protection

1. Try submitting a form without `{% csrf_token %}` - should fail
2. Try submitting with invalid token - should return 403
3. Verify token is present in form HTML source

---

## XSS Protection

### Implementation

#### 1. Browser XSS Filter
```python
SECURE_BROWSER_XSS_FILTER = True
```
- Adds `X-XSS-Protection: 1; mode=block` header
- Enables browser's built-in XSS filtering

#### 2. Content Type Protection
```python
SECURE_CONTENT_TYPE_NOSNIFF = True
```
- Adds `X-Content-Type-Options: nosniff` header
- Prevents MIME-sniffing attacks

#### 3. Template Auto-Escaping
Django templates automatically escape output:
```django
{{ user_input|escape }}  <!-- Explicit escaping -->
{{ user_input }}        <!-- Auto-escaped by default -->
```

#### 4. Form Input Sanitization
Django forms automatically escape HTML in input fields:
```python
form = BookForm(request.POST)
# All form fields are automatically escaped
```

### XSS Prevention Checklist

- ✅ All user input is escaped in templates
- ✅ Forms use Django forms (automatic escaping)
- ✅ Never use `|safe` filter with user input
- ✅ JavaScript is properly escaped
- ✅ URLs are validated before use

---

## SQL Injection Prevention

### Implementation

#### 1. Django ORM (Object-Relational Mapping)
**NEVER use raw SQL with string formatting:**
```python
# ❌ VULNERABLE - SQL Injection risk
Book.objects.raw("SELECT * FROM books WHERE title = '%s'" % user_input)

# ✅ SECURE - Uses parameterized queries
Book.objects.filter(title=user_input)
```

#### 2. Parameterized Queries
Django ORM automatically uses parameterized queries:
```python
# All of these are safe:
Book.objects.get(pk=user_id)
Book.objects.filter(title__icontains=search_query)
Book.objects.create(title=title, author=author)
book.save()  # Updates use parameterized queries
book.delete()  # Deletes use parameterized queries
```

#### 3. Search Functionality
```python
# Secure search using Q objects
from django.db.models import Q

books = Book.objects.filter(
    Q(title__icontains=query) | Q(author__icontains=query)
)
```

### SQL Injection Prevention Checklist

- ✅ Always use Django ORM, never raw SQL
- ✅ If raw SQL is necessary, use parameterized queries
- ✅ Validate and sanitize all user input
- ✅ Use Django forms for input validation
- ✅ Never concatenate user input into SQL strings

---

## Content Security Policy (CSP)

### Implementation

#### 1. Custom Middleware
Location: `bookshelf/middleware.py`

```python
class ContentSecurityPolicyMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        csp_value = "default-src 'self'; script-src 'self' ..."
        response['Content-Security-Policy'] = csp_value
        return response
```

#### 2. CSP Directives
- `default-src 'self'`: Only load resources from same origin
- `script-src 'self'`: Only execute scripts from same origin
- `style-src 'self'`: Only load styles from same origin
- `img-src 'self' data: https:`: Allow images from same origin, data URIs, and HTTPS
- `frame-ancestors 'none'`: Prevents clickjacking

#### 3. Production Considerations
- Remove `'unsafe-inline'` from script-src and style-src
- Remove `'unsafe-eval'` if not needed
- Add specific trusted domains instead of wildcards

### Testing CSP

1. Check response headers for `Content-Security-Policy`
2. Test that inline scripts are blocked (if `'unsafe-inline'` removed)
3. Verify external resources are blocked (if not in allowlist)

---

## Session Security

### Implementation

#### 1. Secure Cookies
```python
SESSION_COOKIE_SECURE = not DEBUG  # True in production
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
```

#### 2. Session Timeout
```python
SESSION_COOKIE_AGE = 1209600  # 2 weeks
```

### Session Security Best Practices

- ✅ Use HTTPS in production (SESSION_COOKIE_SECURE = True)
- ✅ Prevent JavaScript access (SESSION_COOKIE_HTTPONLY = True)
- ✅ Set appropriate session timeout
- ✅ Regenerate session ID on login
- ✅ Clear sessions on logout

---

## Input Validation and Sanitization

### Implementation

#### 1. Django Forms
Location: `bookshelf/forms.py`

```python
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        # Validation logic
        return title.strip()
```

#### 2. Form Validation Features
- Automatic HTML escaping
- Type validation (integers, emails, etc.)
- Length validation (max_length, min_length)
- Custom validation methods (clean_*)
- Sanitization (strip whitespace, remove dangerous patterns)

#### 3. View-Level Validation
```python
if form.is_valid():
    # Form data is validated and sanitized
    book = form.save()
```

### Input Validation Checklist

- ✅ All user input goes through Django forms
- ✅ Custom validation in form clean methods
- ✅ Type checking and range validation
- ✅ Length limits enforced
- ✅ Dangerous patterns detected and rejected
- ✅ Output is escaped in templates

---

## Production Deployment Checklist

Before deploying to production, ensure:

### 1. Environment Variables
```bash
export DEBUG=False
export SECRET_KEY='your-secret-key-here'
export ALLOWED_HOSTS='yourdomain.com,www.yourdomain.com'
export CSRF_TRUSTED_ORIGINS='https://yourdomain.com'
```

### 2. Settings Configuration
- [ ] `DEBUG = False`
- [ ] `SECRET_KEY` from environment variable
- [ ] `ALLOWED_HOSTS` configured with actual domains
- [ ] `CSRF_COOKIE_SECURE = True`
- [ ] `SESSION_COOKIE_SECURE = True`
- [ ] `SECURE_SSL_REDIRECT = True`
- [ ] `SECURE_HSTS_SECONDS = 31536000` (1 year)
- [ ] `SECURE_HSTS_INCLUDE_SUBDOMAINS = True`

### 3. CSP Configuration
- [ ] Remove `'unsafe-inline'` from CSP directives
- [ ] Remove `'unsafe-eval'` if not needed
- [ ] Add specific trusted domains

### 4. Server Configuration
- [ ] HTTPS/SSL certificate configured
- [ ] Web server (nginx/Apache) in front of Django
- [ ] Static files served by web server
- [ ] Database credentials secured
- [ ] Regular security updates applied

### 5. Code Review
- [ ] No raw SQL queries
- [ ] All forms use `{% csrf_token %}`
- [ ] All user input validated
- [ ] No `|safe` filter with user input
- [ ] Proper permission checks in views

---

## Security Testing

### Manual Testing Checklist

1. **CSRF Protection**
   - Submit form without token → Should fail
   - Submit form with invalid token → Should return 403

2. **XSS Protection**
   - Enter `<script>alert('XSS')</script>` in form → Should be escaped
   - Check that script doesn't execute in browser

3. **SQL Injection**
   - Enter `' OR '1'='1` in search → Should be handled safely
   - Check database logs for parameterized queries

4. **Input Validation**
   - Submit empty required fields → Should show errors
   - Submit invalid data types → Should show errors
   - Submit data exceeding max_length → Should be rejected

5. **Permission Checks**
   - Access protected views without permission → Should return 403
   - Test with different user roles

---

## Additional Resources

- [Django Security Documentation](https://docs.djangoproject.com/en/stable/topics/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [Content Security Policy Reference](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)

---

## Security Contact

For security concerns or vulnerabilities, please contact the development team.

**Last Updated**: 2025-11-16

