"""
ASGI config for PK PY CMS project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pkpycms.settings')

application = get_asgi_application()
