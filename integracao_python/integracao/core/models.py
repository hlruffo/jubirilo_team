from django.db import models

# Create your models here.
class DataModel(models.Model):
    data = models.JSONField()