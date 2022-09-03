"""
WSGI config for lighthouse project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os, sys
from django.core.wsgi import get_wsgi_application 



cwd = os.getcwd() 
sys.path.append(cwd) 
sys.path.append(cwd + '/app') 
os.environ['DJANGO_SETTINGS_MODULE'] = "lighthouse.settings" 
application = get_wsgi_application()