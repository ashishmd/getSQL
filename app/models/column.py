from django.db import models


class Columns(models.Model):
    table_id= models.IntegerField()
    column_name = models.CharField(max_length=100)
    is_primary = models.BooleanField(default=0)
    is_indexed = models.BooleanField(default=0)
    foreign_key_column_id = models.IntegerField(null=True)
    foreign_key_table_id = models.IntegerField(null=True)




