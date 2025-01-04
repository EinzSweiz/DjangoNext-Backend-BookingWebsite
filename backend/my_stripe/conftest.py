import os
import django
import tempfile
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status

# Set the default settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.django_backend.settings")

django.setup()

import pytest
from rest_framework.test import APIClient