#!/usr/bin/env python
import os
import sys
import dotenv

def _visual_code_docker_debug():
    try:
        import ptvsd
        if os.environ.get('RUN_MAIN'):
            ptvsd.enable_attach(address=('0.0.0.0', 3003),
                                redirect_output=True)
    except:
        pass

if __name__ == "__main__":
    dotenv.read_dotenv()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vinted_backend.settings")
    os.environ.setdefault("DJANGO_CONFIGURATION", os.getenv('DJANGO_CONFIGURATION'))

    try:
        from configurations.management import execute_from_command_line
        _visual_code_docker_debug()
    except ImportError:
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise

    execute_from_command_line(sys.argv)