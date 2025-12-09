"""
Database connection middleware for Heroku production environment.
Ensures database connections are properly managed and closed to prevent
connection pool exhaustion.
"""
import os
import logging
from django.db import connections

logger = logging.getLogger(__name__)


class HerokuDatabaseMiddleware:
    """
    Middleware to manage database connections for Heroku production environment.
    Closes all database connections after each request to prevent connection leaks.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Only enable when DATABASE_URL is present (Heroku environment)
        self.enabled = bool(os.environ.get("DATABASE_URL"))
        
        if self.enabled:
            logger.info("HerokuDatabaseMiddleware enabled - will close connections after each request")
        
    def __call__(self, request):
        try:
            response = self.get_response(request)
        except Exception as e:
            # Ensure connections are closed even if request fails
            if self.enabled:
                self._close_connections()
            raise
        
        # Close all database connections after each request in production
        if self.enabled:
            self._close_connections()
        
        return response
    
    def _close_connections(self):
        """Helper method to safely close all database connections"""
        try:
            connections.close_all()
            logger.debug("Database connections closed successfully")
        except Exception as e:
            logger.warning(f"Could not close database connections: {e}")
    
    def process_exception(self, request, exception):
        """Ensure connections are closed even if an exception occurs"""
        if self.enabled:
            self._close_connections()
        return None