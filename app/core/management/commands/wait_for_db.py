"""
Django command to wait for the database to be available.
"""

import time

from psycopg2 import OperationalError as Psycopg2OpError

from django.db.utils import OperationalError # Error Django throws when database is not ready

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for the database."""

    def handle(self, *args, **options):
        """"Entrypoint for command."""
        self.stdout.write('Waiting for database...') # this just shows in our console the message waiting for database.
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default']) # by this .check command we check if database ready or not
                # This is that .check method that we mock inside our tests/test_commands.py
                
                db_up = True # as soon as it gets marked as true, 
                # then the while loop will stop because db_up is no longer False and then it will execute line 33

            except (Psycopg2OpError, OperationalError): # if database is not ready we raise an exception
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))

