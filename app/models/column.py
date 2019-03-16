from django.db import models

class Columns(models.Model):
    table_id= models.IntegerField()
    column_name = models.CharField(max_length=100)
    is_primary = models.IntegerField(default=0)
    is_indexed = models.IntegerField(default=0)
    foreign_key_column_id = models.IntegerField(default=None)
    foreign_key_table_id = models.IntegerField(default=None)




