# Create your models here.
from django.db import models


class Tables(models.Model):
    table_name = models.CharField(max_length=100)
    alias = models.CharField(max_length=100)

