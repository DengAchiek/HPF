"""
Root-level WSGI shim for hosts that run commands from the repository root.

Render may start this project with:
    gunicorn Health_Planet.wsgi:application

The actual Django project package lives one level deeper at
Health_Planet/Health_Planet, so this shim points Python at the inner package
while preserving the normal local command layout.
"""

import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PROJECT_PACKAGE_DIR = BASE_DIR / "Health_Planet"

sys.path.insert(0, str(BASE_DIR))

import Health_Planet as package  # noqa: E402

package.__path__ = [str(PROJECT_PACKAGE_DIR), *list(getattr(package, "__path__", []))]

from django.core.wsgi import get_wsgi_application  # noqa: E402

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Health_Planet.settings")

application = get_wsgi_application()
