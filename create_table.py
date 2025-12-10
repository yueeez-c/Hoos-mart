
from django.db import connection

with connection.cursor() as cursor:
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_banneduser (
            id SERIAL PRIMARY KEY,
            email VARCHAR(254) UNIQUE NOT NULL,
            banned_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
        );
    ''')
    print('user_banneduser table created successfully!')
