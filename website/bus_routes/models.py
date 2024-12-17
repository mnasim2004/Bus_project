# models.py (if you plan to use database)
from django.db import models

class Stop(models.Model):
    name = models.CharField(max_length=255)
    grid = models.CharField(max_length=10)
    color = models.CharField(max_length=50)
