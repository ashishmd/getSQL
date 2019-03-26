# Purpose of this table is to store th type of relations - has_one/has_many/many_to_many
from django.db import models


class Relations(models.Model):
    table_1_id = models.IntegerField()
    table_2_id = models.IntegerField()
    type = models.IntegerField()
    link_table = models.IntegerField(null=True)
