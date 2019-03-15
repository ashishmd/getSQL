from django.db import models
from app.models import Tables

class Columns(models.Model):
    table_id= models.ForgeinKey(Tables,max_length=100)
    column_name = models.CharField(max_length=100)
    is_primary = models.IntegerField(default=0)
    is_indexed = models.IntegerField(default=0)
    foreign_key_column_id = models.IntegerField(max_length=100,default=0)
    foreign_key_table_name = models.CharField(max_length=100,default=0)




