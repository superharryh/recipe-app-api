"""
Test Custom Django management commands.
"""

from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2OpError

from django.core.management import call_command

from django.db.utils import OperationalError

from django.test import SimpleTestCase

# mock that behavior by doing @patch():
@patch('core.management.commands.wait_for_db.Command.check') # this is basically the command that we're going to be mocking
class CommandTests(SimpleTestCase):
    """Test commands."""

    def test_wait_for_db_ready(self, patched_check): # patched_check = @patch('core.management.commands.wait_for_db.Command.check')
        """Test waiting for database if database ready."""
        patched_check.return_value = True # when check is called inside our command, inside our TestCase,
        # we just want it to return the true value.

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])
    
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError."""
        patched_check.side_effect = [Psycopg2OpError] * 2 + \
            [OperationalError] * 3 + [True] 
        # first two times when we call the mocked method (core.management.commands.wait_for_db.Command.check) 
        # we want it to raise the Psycopg2OpError. Then what we do is we raise three OperationalError.
        # So the first two times we raise the Psycopg2OpError and the next three times we raise OperationalError.

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])


