"""
Management command to create missing user_banneduser table
"""
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Create missing user_banneduser table'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            # Create the table if it doesn't exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_banneduser (
                    id SERIAL PRIMARY KEY,
                    email VARCHAR(254) UNIQUE NOT NULL,
                    banned_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
                );
            ''')
            
        self.stdout.write(self.style.SUCCESS('✓ user_banneduser table created successfully!'))
