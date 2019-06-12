# Create your models here.
from django.db import models
from django_mysql.models import JSONField, Model


class Path(Model):
    base_table_id = models.IntegerField()
    final_table_id = models.IntegerField()
    path = JSONField()

