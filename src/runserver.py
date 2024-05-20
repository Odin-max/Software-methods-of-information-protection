import os
import sys
from django.core.management import execute_from_command_line

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
        from django.utils.autoreload import run_with_reloader
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Disable the autoreloader for PyInstaller compatibility
    def no_reloader(args):
        execute_from_command_line(args)

    # Check if the autoreloader should be disabled
    if 'runserver' in sys.argv:
        run_with_reloader(no_reloader, sys.argv)
    else:
        execute_from_command_line(sys.argv)


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management.commands.runserver import Command as runserver
        runserver.default_addr = '127.0.0.1'
        runserver.default_port = '8000'
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Apply migrations before starting the server
    execute_from_command_line([sys.argv[0], 'migrate'])
    
    # Start the server
    execute_from_command_line([sys.argv[0], 'runserver', '127.0.0.1:8000', '--noreload'])
