# HTTPS Deployment Configuration Guide

This document provides step-by-step instructions for deploying the LibraryProject Django application with HTTPS/SSL support.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [SSL/TLS Certificate Setup](#ssltls-certificate-setup)
3. [Nginx Configuration](#nginx-configuration)
4. [Apache Configuration](#apache-configuration)
5. [Django Settings Configuration](#django-settings-configuration)
6. [Testing HTTPS Setup](#testing-https-setup)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before configuring HTTPS, ensure you have:

- Django application deployed and running
- Domain name pointing to your server
- Root or sudo access to the server
- Web server (Nginx or Apache) installed
- SSL/TLS certificate (from Let's Encrypt, commercial CA, or self-signed for testing)

---

## SSL/TLS Certificate Setup

### Option 1: Let's Encrypt (Recommended for Production)

Let's Encrypt provides free SSL certificates that are trusted by all major browsers.

#### Install Certbot

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx  # For Nginx
sudo apt-get install certbot python3-certbot-apache  # For Apache

# CentOS/RHEL
sudo yum install certbot python3-certbot-nginx  # For Nginx
sudo yum install certbot python3-certbot-apache  # For Apache
```

#### Obtain Certificate

```bash
# For Nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# For Apache
sudo certbot --apache -d yourdomain.com -d www.yourdomain.com

# Standalone (if web server not configured yet)
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com
```

Certificates are typically stored in:
- `/etc/letsencrypt/live/yourdomain.com/fullchain.pem`
- `/etc/letsencrypt/live/yourdomain.com/privkey.pem`

#### Auto-Renewal

Certbot sets up automatic renewal. Test it:

```bash
sudo certbot renew --dry-run
```

### Option 2: Commercial SSL Certificate

If using a commercial certificate provider:

1. Purchase and download your SSL certificate
2. Upload certificate files to your server
3. Note the paths to:
   - Certificate file (`.crt` or `.pem`)
   - Private key file (`.key`)
   - Certificate chain file (if provided)

### Option 3: Self-Signed Certificate (Testing Only)

**WARNING**: Self-signed certificates are NOT suitable for production. Use only for development/testing.

```bash
# Generate self-signed certificate
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/ssl/private/nginx-selfsigned.key \
  -out /etc/ssl/certs/nginx-selfsigned.crt
```

---

## Nginx Configuration

### Basic HTTPS Configuration

Create or edit `/etc/nginx/sites-available/libraryproject`:

```nginx
# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    # Redirect all HTTP requests to HTTPS
    return 301 https://$server_name$request_uri;
}

# HTTPS Server Configuration
server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    
    # SSL Certificate Configuration
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    # SSL Configuration - Strong Security Settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384';
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    ssl_session_tickets off;
    
    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    
    # Root and Index
    root /var/www/libraryproject;
    index index.html;
    
    # Logging
    access_log /var/log/nginx/libraryproject_access.log;
    error_log /var/log/nginx/libraryproject_error.log;
    
    # Static Files
    location /static/ {
        alias /path/to/your/project/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    # Media Files
    location /media/ {
        alias /path/to/your/project/media/;
        expires 30d;
        add_header Cache-Control "public";
    }
    
    # Django Application
    location / {
        proxy_pass http://127.0.0.1:8000;  # Gunicorn/uWSGI
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $server_name;
        
        # WebSocket support (if needed)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### Enable Site and Test Configuration

```bash
# Create symbolic link
sudo ln -s /etc/nginx/sites-available/libraryproject /etc/nginx/sites-enabled/

# Test Nginx configuration
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx
```

---

## Apache Configuration

### Basic HTTPS Configuration

Create or edit `/etc/apache2/sites-available/libraryproject.conf`:

```apache
# Redirect HTTP to HTTPS
<VirtualHost *:80>
    ServerName yourdomain.com
    ServerAlias www.yourdomain.com
    
    # Redirect all HTTP requests to HTTPS
    Redirect permanent / https://yourdomain.com/
</VirtualHost>

# HTTPS Server Configuration
<VirtualHost *:443>
    ServerName yourdomain.com
    ServerAlias www.yourdomain.com
    
    # SSL Certificate Configuration
    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/yourdomain.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/yourdomain.com/privkey.pem
    
    # SSL Configuration
    SSLProtocol all -SSLv3 -TLSv1 -TLSv1.1
    SSLCipherSuite ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384
    SSLHonorCipherOrder off
    
    # Security Headers
    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
    Header always set X-Frame-Options "DENY"
    Header always set X-Content-Type-Options "nosniff"
    Header always set X-XSS-Protection "1; mode=block"
    Header always set Referrer-Policy "strict-origin-when-cross-origin"
    
    # Logging
    ErrorLog ${APACHE_LOG_DIR}/libraryproject_error.log
    CustomLog ${APACHE_LOG_DIR}/libraryproject_access.log combined
    
    # Static Files
    Alias /static /path/to/your/project/staticfiles
    <Directory /path/to/your/project/staticfiles>
        Require all granted
    </Directory>
    
    # Media Files
    Alias /media /path/to/your/project/media
    <Directory /path/to/your/project/media>
        Require all granted
    </Directory>
    
    # Django Application
    WSGIDaemonProcess libraryproject python-home=/path/to/venv python-path=/path/to/project
    WSGIProcessGroup libraryproject
    WSGIScriptAlias / /path/to/project/LibraryProject/wsgi.py
    
    <Directory /path/to/project/LibraryProject>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>
</VirtualHost>
```

### Enable Required Modules

```bash
# Enable SSL and headers modules
sudo a2enmod ssl
sudo a2enmod headers
sudo a2enmod rewrite

# Enable site
sudo a2ensite libraryproject.conf

# Test Apache configuration
sudo apache2ctl configtest

# Restart Apache
sudo systemctl restart apache2
```

---

## Django Settings Configuration

### Environment Variables

Set the following environment variables on your production server:

```bash
# .env file or export commands
export DEBUG=False
export SECRET_KEY='your-secret-key-here'
export ALLOWED_HOSTS='yourdomain.com,www.yourdomain.com'
export CSRF_TRUSTED_ORIGINS='https://yourdomain.com,https://www.yourdomain.com'

# HTTPS Settings
export SECURE_SSL_REDIRECT=True
export SECURE_HSTS_SECONDS=31536000
export SECURE_HSTS_INCLUDE_SUBDOMAINS=True
export SECURE_HSTS_PRELOAD=True

# Secure Cookies
export CSRF_COOKIE_SECURE=True
export SESSION_COOKIE_SECURE=True
```

### Using .env File

Create a `.env` file in your project root:

```bash
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
CSRF_COOKIE_SECURE=True
SESSION_COOKIE_SECURE=True
```

Load environment variables in `settings.py` (if using python-decouple or similar):

```python
from decouple import config

SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=False, cast=bool)
```

---

## Testing HTTPS Setup

### 1. Test SSL Certificate

```bash
# Check certificate validity
openssl s_client -connect yourdomain.com:443 -servername yourdomain.com

# Test SSL configuration
ssl Labs: https://www.ssllabs.com/ssltest/analyze.html?d=yourdomain.com
```

### 2. Test HTTP to HTTPS Redirect

```bash
# Should redirect to HTTPS
curl -I http://yourdomain.com

# Should return 200 OK
curl -I https://yourdomain.com
```

### 3. Test Security Headers

```bash
# Check security headers
curl -I https://yourdomain.com | grep -i "strict-transport-security\|x-frame-options\|x-content-type-options"
```

### 4. Test HSTS

1. Visit your site in a browser
2. Open Developer Tools → Network tab
3. Check response headers for `Strict-Transport-Security`
4. Clear browser cache and visit again - should use HTTPS automatically

---

## Troubleshooting

### Common Issues

#### 1. Mixed Content Warnings

**Problem**: Browser blocks HTTP resources on HTTPS page

**Solution**: Ensure all resources (CSS, JS, images) are loaded over HTTPS

#### 2. Certificate Errors

**Problem**: Browser shows certificate warning

**Solution**: 
- Verify certificate is valid and not expired
- Check certificate chain is complete
- Ensure domain matches certificate

#### 3. Infinite Redirect Loop

**Problem**: Site redirects infinitely

**Solution**:
- Check `SECURE_SSL_REDIRECT` is not conflicting with web server redirect
- Verify proxy headers are set correctly (`X-Forwarded-Proto`)
- Ensure Django sees requests as HTTPS

#### 4. Cookies Not Working

**Problem**: Session/CSRF cookies not set

**Solution**:
- Verify `SESSION_COOKIE_SECURE` and `CSRF_COOKIE_SECURE` are True
- Check cookies are being sent over HTTPS
- Verify domain settings in cookies

### Debugging Commands

```bash
# Check Nginx error logs
sudo tail -f /var/log/nginx/error.log

# Check Apache error logs
sudo tail -f /var/log/apache2/error.log

# Test Django settings
python manage.py check --deploy

# Verify environment variables
env | grep SECURE
```

---

## Additional Resources

- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)
- [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/)
- [OWASP Transport Layer Protection Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Protection_Cheat_Sheet.html)

---

**Last Updated**: 2025-11-16

