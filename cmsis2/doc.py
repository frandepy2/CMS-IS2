import django
import pydoc
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cmsis2.settings")

application = get_wsgi_application()

django.setup()
pydoc.cli()

# ejecutar python cmsis2/doc.py -b