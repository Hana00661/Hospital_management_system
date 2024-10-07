from django.db import models
from mainapp import models as base_models

def default():
    services = base_models.Service.objects.all()

    return {
        "services": services
    }