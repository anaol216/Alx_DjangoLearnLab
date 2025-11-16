"""
Custom middleware for Content Security Policy (CSP) headers.

This middleware adds CSP headers to all responses to help prevent
XSS (Cross-Site Scripting) attacks by controlling which resources
can be loaded by the browser.
"""

from django.utils.deprecation import MiddlewareMixin


class ContentSecurityPolicyMiddleware(MiddlewareMixin):
    """
    Middleware to add Content Security Policy headers.
    
    CSP helps prevent XSS attacks by specifying which domains can be used
    to load scripts, stylesheets, images, and other resources.
    
    Usage:
    Add 'bookshelf.middleware.ContentSecurityPolicyMiddleware' to MIDDLEWARE
    in settings.py (after SecurityMiddleware).
    """
    
    def process_response(self, request, response):
        """
        Add CSP headers to the response.
        
        CSP Directives:
        - default-src: Fallback for other directives
        - script-src: Controls JavaScript execution
        - style-src: Controls CSS stylesheets
        - img-src: Controls image loading
        - font-src: Controls font loading
        - connect-src: Controls AJAX/fetch requests
        - frame-ancestors: Controls iframe embedding (replaces X-Frame-Options)
        """
        
        # Build CSP header value
        # In production, remove 'unsafe-inline' and 'unsafe-eval' for better security
        csp_directives = [
            "default-src 'self'",
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'",  # Remove 'unsafe-inline' in production
            "style-src 'self' 'unsafe-inline'",  # Remove 'unsafe-inline' in production
            "img-src 'self' data: https:",
            "font-src 'self' data:",
            "connect-src 'self'",
            "frame-ancestors 'none'",  # Prevents embedding (clickjacking protection)
            "base-uri 'self'",
            "form-action 'self'",
        ]
        
        # Join directives with semicolon
        csp_value = "; ".join(csp_directives)
        
        # Add CSP header to response
        response['Content-Security-Policy'] = csp_value
        
        # Also add X-Content-Security-Policy for older browsers (deprecated but still used)
        response['X-Content-Security-Policy'] = csp_value
        
        return response

