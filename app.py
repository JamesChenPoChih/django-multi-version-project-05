import os

from django.core.wsgi import get_wsgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

# Compatibility entrypoint for Render services still configured with:
# gunicorn app:app
app = get_wsgi_application()
