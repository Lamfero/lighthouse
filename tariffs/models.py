from django.db import models

# Create your models here.
class TariffSettings(models.Model):
    name = models.CharField(max_length=40, null=True)
    level = models.CharField(max_length=1, null=True)
    description = models.TextField(null=True)
    price = models.CharField(max_length=40, default="600")