import os
import django
import json
from manage import DEFAULT_SETTINGS_MODULE
os.environ.setdefault("DJANGO_SETTINGS_MODULE", DEFAULT_SETTINGS_MODULE)
django.setup()
from datacaptureapp.models import *


def generate(name):

    print(Project.objects.all())
    print(Project.objects.first())
    
    return "whaa eind"


print(generate("TestProject"))