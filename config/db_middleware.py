"""
Database connection middleware for Heroku production environment.
Ensures database connections are properly managed and closed to prevent
connection pool exhaustion.
"""
import os
from django.db import connections
from django.core.exceptions import ImproperlyConfigured


class HerokuDatabaseMiddleware:
    """
    Middleware to manage database connections for Heroku production environment.
    Closes all database connections after each request to prevent connection leaks.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Only enable in production/Heroku environment
        self.enabled = bool(os.environ.get("DATABASE_URL")) and not os.environ.get("DEBUG", "False").lower() == "true"
        
    def __call__(self, request):
        response = self.get_response(request)
        
        # Close all database connections after each request in production
        if self.enabled:
            try:
                connections.close_all()
            except Exception as e:
                # Log but don't crash the app
                print(f"Warning: Could not close database connections: {e}")
        
        return response
    
    def process_exception(self, request, exception):
        """Ensure connections are closed even if an exception occurs"""
        if self.enabled:
            try:
                connections.close_all()
            except Exception:
                pass  # Ignore errors during cleanup
        return None