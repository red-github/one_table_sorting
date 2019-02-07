from django.db import models


class Module(models.Model):
    name = models.CharField(max_length=250)
    parent_id = models.IntegerField(null=False, blank=False)
    sort_id = models.IntegerField()

    class Meta:
        db_table = 'modules'
